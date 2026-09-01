import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from models.converter_physics import cap_vout_ss
from models.cm2_physics import (
    VI_I_MAX, VI_V_MAX, CHRONO_Y, solve, i_L_period, dcm_boundary,
)
from i18n import t
from callbacks.figure_helpers import (
    C_RED, C_ORANGE, C_GRAY, C_DARK_BLUE, C_PURPLE,
    C_VOUT, C_IOUT, C_VIN, C_IIN,
    setup_vi_figure, setup_chrono_figure, add_operating,
)

_CIRCUIT_IMG_SRC = {
    'buck_transistor': '/assets/Buck_chopper_1.drawio.png',
    'buck_diode': '/assets/Buck_chopper_2.drawio.png',
    'boost_transistor': '/assets/Boost_chopper_1.drawio.png',
    'boost_diode': '/assets/Boost_chopper_2.drawio.png',
}


def _circuit_img_src(mode, sw):
    return _CIRCUIT_IMG_SRC.get(f'{mode}_{sw}', '')


def build_vi(mode, E, R, D, L, sw, T, C, show_iminmax=False, show_dcm=True, lang='fr'):
    v_out, i_out_avg, i_in_avg, i_pk, i_lo, _ = solve(mode, E, R, D, L, sw, T)
    if show_iminmax:
        phase, i_L, i_in_1p, i_out_1p, *_ = i_L_period(mode, E, R, D, L, sw, T)
        dt = T / len(phase)
        v_ss = cap_vout_ss(i_out_1p, R, C, dt)
        v_hi_raw = np.max(v_ss)
        v_lo_raw = max(np.min(v_ss), 0.0)
    i_max, v_max = VI_I_MAX, VI_V_MAX

    fig = setup_vi_figure(lang, i_max, v_max)

    if show_dcm and sw == 'diode':
        # DCM only exists with a diode T2 — a transistor is always driven CCM regardless
        # of load, so the boundary/zone is meaningless (and misleading) in that mode.
        f = 1.0 / T
        V_b, I_b = dcm_boundary(mode, E, L, f, v_max)
        I_b_c = np.clip(I_b, 0, i_max)
        fig.add_trace(go.Scatter(x=I_b_c, y=V_b, mode='lines', fill='tozerox',
                                  line=dict(color=C_ORANGE, width=1.3, dash='dash'),
                                  fillcolor='rgba(224,123,0,0.14)', opacity=0.75,
                                  name=t('dcm_zone_label', lang)))

    i_r = np.linspace(0, i_max, 400)
    fig.add_trace(go.Scatter(x=i_r, y=np.clip(i_r * R, 0, v_max), mode='lines',
                              line=dict(color=C_DARK_BLUE, width=1.2), opacity=0.5,
                              name=t('charge_r', lang, R=R)))
    add_operating(fig, i_out=i_out_avg, v_out=v_out, i_in=i_in_avg, v_in=E, avg=True,
                  i_max=i_max, v_max=v_max)

    if show_iminmax:
        v_hi = min(v_hi_raw, v_max)
        v_lo = min(v_lo_raw, v_max)
        p_hi = v_hi ** 2 / R
        p_lo = v_lo ** 2 / R
        fig.add_trace(go.Scatter(x=[min(v_hi / R, i_max)], y=[v_hi], mode='markers',
                                  marker=dict(symbol='triangle-up', size=11, color=C_ORANGE),
                                  name=f'P_max = {p_hi:.1f} W'))
        fig.add_trace(go.Scatter(x=[v_lo / R], y=[v_lo], mode='markers',
                                  marker=dict(symbol='triangle-down', size=11, color=C_ORANGE),
                                  name=f'P_min = {p_lo:.1f} W'))
    return fig


def build_chrono(mode, E, R, D, L, sw, T, C, show_iminmax=False, lang='fr'):
    (phase, i_L, i_in_1p, i_out_1p, v_out, i_out_avg, i_in_avg,
     i_pk, i_lo, ccm) = i_L_period(mode, E, R, D, L, sw, T)

    dt = T / len(phase)
    v_ss = cap_vout_ss(i_out_1p, R, C, dt)

    t_norm = np.tile(phase / T, 2) + np.repeat([0, 1], len(phase))
    i_L_2p = np.tile(i_L, 2)
    i_in_2p = np.tile(i_in_1p, 2)
    i_out_2p = np.tile(i_out_1p, 2)
    v_out_wave = np.tile(v_ss, 2)

    # A small output cap (esp. boost, pulsed charging) can ripple past the nominal scale —
    # widen the axis rather than clip the waveform.
    y_top = max(CHRONO_Y, float(np.max(v_out_wave)) * 1.08, E * 1.1)
    y_bot = min(-0.5, float(np.min(v_out_wave)) - 1.0)

    fig = setup_chrono_figure(lang, y_range=(y_bot, y_top), x_title=t('axis_time_norm', lang))

    fig.add_trace(go.Scatter(x=t_norm, y=v_out_wave, mode='lines', line=dict(color=C_VOUT, width=2),
                              name=t('vout_avg', lang, v_out=v_out)))
    fig.add_trace(go.Scatter(x=t_norm, y=i_L_2p, mode='lines',
                              line=dict(color=C_PURPLE, dash='dashdot', width=1.6), opacity=0.85,
                              name=t('il_avg', lang, i_avg=(i_out_avg if mode == 'buck' else i_in_avg))))
    fig.add_trace(go.Scatter(x=t_norm, y=i_out_2p, mode='lines', line=dict(color=C_IOUT, dash='dash', width=2),
                              name=t('iout_avg', lang, i_out_avg=i_out_avg)))
    fig.add_trace(go.Scatter(x=[t_norm[0], t_norm[-1]], y=[E, E], mode='lines',
                              line=dict(color=C_VIN, dash='dot', width=1.8), name=f'V_IN  = {E:.2f} V'))
    fig.add_trace(go.Scatter(x=t_norm, y=i_in_2p, mode='lines', line=dict(color=C_IIN, dash='dashdot', width=2),
                              name=t('iin_avg', lang, i_in_avg=i_in_avg)))

    fig.add_hline(y=v_out, line=dict(color=C_VOUT, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=i_out_avg, line=dict(color=C_IOUT, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=i_in_avg, line=dict(color=C_IIN, dash='dot', width=1), opacity=0.55)

    if show_iminmax:
        fig.add_trace(go.Scatter(x=[t_norm[0], t_norm[-1]], y=[i_pk, i_pk], mode='lines',
                                  line=dict(color=C_PURPLE, dash='dash', width=1.2), opacity=0.9,
                                  name=f'i_L,max = {i_pk:.2f} A'))
        fig.add_trace(go.Scatter(x=[t_norm[0], t_norm[-1]], y=[i_lo, i_lo], mode='lines',
                                  line=dict(color=C_PURPLE, dash='dash', width=1.2), opacity=0.9,
                                  name=f'i_L,min = {i_lo:.2f} A'))

    for k in (0, 1):
        fig.add_vline(x=k + D, line=dict(color=C_GRAY, dash='dot', width=0.8), opacity=0.5)
    fig.add_annotation(x=D / 2, y=y_bot + 0.2, text='D·T', showarrow=False, font=dict(size=8, color=C_GRAY))

    if not ccm:
        fig.add_annotation(text=t('dcm_banner2', lang), x=0.03, y=0.96, xref='paper', yref='paper',
                            showarrow=False, font=dict(size=10, color=C_PURPLE), align='left',
                            xanchor='left', yanchor='top',
                            bgcolor='#f3e8ff', bordercolor=C_PURPLE, borderwidth=1)
    return fig


def build_voutd(mode, E, R, D, L, sw, T, lang='fr'):
    D_r = np.linspace(0.02, 0.98, 300)
    v_ideal = np.where(D_r < 0.999, E * D_r, np.nan) if mode == 'buck' \
        else E / np.clip(1.0 - D_r, 1e-6, None)

    v_actual = np.empty_like(D_r)
    ccm_mask = np.empty_like(D_r, dtype=bool)
    for i, d in enumerate(D_r):
        v_actual[i], _, _, _, _, ccm_mask[i] = solve(mode, E, R, d, L, sw, T)

    y_max = E * 1.15 if mode == 'buck' else min(np.nanmax(v_actual) * 1.35, E * 8)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=D_r, y=np.clip(v_ideal, 0, y_max * 1.3), mode='lines',
                              line=dict(color=C_GRAY, dash='dash', width=1.2), opacity=0.7,
                              name=t('voutd_ideal', lang)))
    v_ccm = np.where(ccm_mask, v_actual, np.nan)
    v_dcm = np.where(~ccm_mask, v_actual, np.nan)
    fig.add_trace(go.Scatter(x=D_r, y=v_ccm, mode='lines', line=dict(color=C_VOUT, width=2.2),
                              name=t('voutd_ccm', lang)))
    fig.add_trace(go.Scatter(x=D_r, y=v_dcm, mode='lines', line=dict(color=C_ORANGE, width=2.2),
                              name=t('voutd_dcm', lang)))

    v_now, _, _, _, _, ccm_now = solve(mode, E, R, D, L, sw, T)
    fig.add_vline(x=D, line=dict(color=C_RED, dash='dash', width=1.1), opacity=0.7)
    fig.add_trace(go.Scatter(x=[D], y=[v_now], mode='markers',
                              marker=dict(symbol='circle', size=11, color=C_RED),
                              name=t('voutd_operating', lang, v_now=v_now,
                                     regime=('CCM' if ccm_now else 'DCM'))))

    fig.update_layout(
        xaxis=dict(title=t('axis_duty', lang), range=[0, 1], gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title='V_OUT (V)', range=[0, max(y_max, E * 1.1)], gridcolor='rgba(0,0,0,0.1)'),
        title=t('voutd_title', lang),
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=50, r=20, t=40, b=40),
        legend=dict(x=0.02, y=0.98, xanchor='left', yanchor='top', font=dict(size=9)),
    )
    return fig


def register_cm2_plot_callback(app):
    @app.callback(
        Output('cm2-circuit-img', 'src'),
        Output('cm2-vi-plane-graph', 'figure'),
        Output('cm2-chrono-graph', 'figure'),
        Output('cm2-voutd-graph', 'figure'),
        Input('cm2-mode-select', 'value'),
        Input('cm2-t2-select', 'value'),
        Input('cm2-show-iminmax', 'value'),
        Input('cm2-show-dcmzone', 'value'),
        Input('cm2-slider-E', 'value'),
        Input('cm2-slider-R', 'value'),
        Input('cm2-slider-D', 'value'),
        Input('cm2-slider-L', 'value'),
        Input('cm2-slider-F', 'value'),
        Input('cm2-slider-C', 'value'),
        Input('lang-store', 'data'),
    )
    def update_plots(mode, sw, show_iminmax_val, show_dcmzone_val, E, r_log, D, l_log, f_log, c_log, lang):
        R = 10 ** r_log
        L = 10 ** l_log
        F = 10 ** f_log
        T = 1.0 / F
        C = 10 ** c_log
        show_iminmax = bool(show_iminmax_val)
        show_dcmzone = bool(show_dcmzone_val)
        lang = lang or 'fr'

        vi_fig = build_vi(mode, E, R, D, L, sw, T, C, show_iminmax, show_dcmzone, lang)
        chrono_fig = build_chrono(mode, E, R, D, L, sw, T, C, show_iminmax, lang)
        voutd_fig = build_voutd(mode, E, R, D, L, sw, T, lang)
        img_src = _circuit_img_src(mode, sw)
        return img_src, vi_fig, chrono_fig, voutd_fig
