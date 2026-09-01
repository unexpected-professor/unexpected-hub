import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from models.converter_physics import (
    VI_I_MAX, VI_V_MAX, T_S, CHRONO_Y, buck_solve, buck_i_L_period, cap_vout_ss,
)
from i18n import t
from callbacks.figure_helpers import (
    C_ORANGE, C_GRAY, C_DARK_BLUE, C_PURPLE,
    C_VOUT, C_IOUT, C_VIN, C_IIN,
    setup_vi_figure, setup_chrono_figure, add_operating,
)

_CIRCUIT_IMG_SRC = {
    'direct': '/assets/case_1.drawio.png',
    'rth': '/assets/case_2.drawio.png',
    'switch': '/assets/case_3.drawio.png',
    'buck_transistor': '/assets/case_4.drawio.png',
    'buck_diode': '/assets/case_4_D.drawio.png',
    'cap_transistor': '/assets/case_5.drawio.png',
    'cap_diode': '/assets/case_5_D.drawio.png',
}


def _circuit_img_src(mode, t2):
    key = f'{mode}_{t2}' if mode in ('buck', 'cap') else mode
    return _CIRCUIT_IMG_SRC.get(key, '')


def build_vi_direct(E, R, lang='fr'):
    i_op = E / R
    i_max, v_max = VI_I_MAX, VI_V_MAX
    fig = setup_vi_figure(lang, i_max, v_max)
    i_r = np.linspace(0, i_max, 400)
    fig.add_trace(go.Scatter(x=i_r, y=np.clip(i_r * R, 0, v_max), mode='lines',
                              line=dict(color=C_DARK_BLUE, width=1.2), opacity=0.5,
                              name=t('charge_r', lang, R=R)))
    add_operating(fig, i_out=i_op, v_out=E, i_in=i_op, v_in=E, i_max=i_max, v_max=v_max)
    return fig


def build_chrono_direct(E, R, lang='fr'):
    fig = setup_chrono_figure(lang)
    t = np.linspace(0, 2, 500)
    i = E / R
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, E), mode='lines',
                              line=dict(color=C_VOUT, width=2), name=f'V_OUT = {E:.2f} V'))
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, i), mode='lines',
                              line=dict(color=C_IOUT, dash='dash', width=2), name=f'I_OUT = {i:.2f} A'))
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, E), mode='lines',
                              line=dict(color=C_VIN, dash='dot', width=1.8), name=f'V_IN  = {E:.2f} V'))
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, i), mode='lines',
                              line=dict(color=C_IIN, dash='dashdot', width=2), name=f'I_IN  = {i:.2f} A'))
    return fig


def build_vi_rth(E, R, Rth, lang='fr'):
    i_op = E / (R + Rth)
    v_op = E * R / (R + Rth)
    i_max, v_max = VI_I_MAX, VI_V_MAX
    fig = setup_vi_figure(lang, i_max, v_max)
    i_r = np.linspace(0, i_max, 400)
    fig.add_trace(go.Scatter(x=i_r, y=np.clip(i_r * R, 0, v_max), mode='lines',
                              line=dict(color=C_DARK_BLUE, width=1.2), opacity=0.5,
                              name=t('charge_r', lang, R=R)))
    i_end = E / max(Rth, 0.01)
    i_th = np.linspace(0, min(i_end, i_max), 300)
    fig.add_trace(go.Scatter(x=i_th, y=np.clip(E - i_th * Rth, 0, v_max), mode='lines',
                              line=dict(color=C_PURPLE, width=1.0, dash='dash'), opacity=0.35,
                              name='V = E - i·Rth'))
    add_operating(fig, i_out=i_op, v_out=v_op, i_in=i_op, v_in=E, i_max=i_max, v_max=v_max)
    return fig


def build_chrono_rth(E, R, Rth, lang='fr'):
    fig = setup_chrono_figure(lang)
    i_op = E / (R + Rth)
    v_op = i_op * R
    t = np.linspace(0, 2, 500)
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, v_op), mode='lines',
                              line=dict(color=C_VOUT, width=2), name=f'V_OUT = {v_op:.2f} V'))
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, i_op), mode='lines',
                              line=dict(color=C_IOUT, dash='dash', width=2), name=f'I_OUT = {i_op:.2f} A'))
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, E), mode='lines',
                              line=dict(color=C_VIN, dash='dot', width=1.8), name=f'V_IN  = {E:.2f} V'))
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, i_op), mode='lines',
                              line=dict(color=C_IIN, dash='dashdot', width=2), name=f'I_IN  = {i_op:.2f} A'))
    return fig


def build_vi_switch(E, R, D, show_iminmax=False, lang='fr'):
    # RMS values for a square wave: V_RMS = E*sqrt(D), I_RMS = (E/R)*sqrt(D)
    v_rms = E * np.sqrt(D)
    i_rms = v_rms / R
    # Input: V_IN = E (constant DC) -> P_in = E x I_avg = E^2*D/R = P_out
    # Must use average current for input, not RMS, to land on the same iso-power curve.
    i_avg = D * E / R
    i_max, v_max = VI_I_MAX, VI_V_MAX
    fig = setup_vi_figure(lang, i_max, v_max)
    i_r = np.linspace(0, i_max, 400)
    fig.add_trace(go.Scatter(x=i_r, y=np.clip(i_r * R, 0, v_max), mode='lines',
                              line=dict(color=C_DARK_BLUE, width=1.2), opacity=0.5,
                              name=t('charge_r', lang, R=R)))
    add_operating(fig, i_out=i_rms, v_out=v_rms, i_in=i_avg, v_in=E, i_max=i_max, v_max=v_max)
    if show_iminmax:
        p_max = (E / R) * E
        fig.add_trace(go.Scatter(x=[E / R], y=[E], mode='markers',
                                  marker=dict(symbol='triangle-up', size=11, color=C_ORANGE),
                                  name=f'P_max = {p_max:.1f} W  {t("k_closed", lang)}'))
        fig.add_trace(go.Scatter(x=[0.0], y=[0.0], mode='markers',
                                  marker=dict(symbol='triangle-down', size=11, color=C_ORANGE),
                                  name=f'P_min = 0 W  {t("k_open", lang)}'))
    return fig


def build_chrono_switch(E, R, D, show_iminmax=False, lang='fr'):
    fig = setup_chrono_figure(lang)
    t_arr = np.linspace(0, 2, 2000)
    T = 1.0
    v_out = np.where((t_arr % T) < D * T, E, 0.0)
    i_out = v_out / R
    v_rms = E * np.sqrt(D)
    i_rms = v_rms / R
    fig.add_trace(go.Scatter(x=t_arr, y=v_out, mode='lines', line=dict(color=C_VOUT, width=2),
                              name=t('vout_pulsed_fem', lang, v_rms=v_rms)))
    fig.add_trace(go.Scatter(x=t_arr, y=i_out, mode='lines', line=dict(color=C_IOUT, dash='dash', width=2),
                              name=t('iout_pulsed', lang, i_rms=i_rms)))
    fig.add_trace(go.Scatter(x=t_arr, y=np.full_like(t_arr, E), mode='lines',
                              line=dict(color=C_VIN, dash='dot', width=1.8), name=f'V_IN  = {E:.2f} V'))
    fig.add_trace(go.Scatter(x=t_arr, y=i_out, mode='lines', line=dict(color=C_IIN, dash='dashdot', width=2),
                              name=t('iin_pulsed_rms', lang, i_rms=i_rms)))
    fig.add_hline(y=v_rms, line=dict(color=C_VOUT, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=i_rms, line=dict(color=C_IOUT, dash='dot', width=1), opacity=0.55)
    if show_iminmax:
        i_max = E / R
        fig.add_trace(go.Scatter(x=[0, 2], y=[i_max, i_max], mode='lines',
                                  line=dict(color=C_IOUT, dash='dash', width=1.2), opacity=0.9,
                                  name=f'I_max = {i_max:.2f} A'))
        fig.add_trace(go.Scatter(x=[0, 2], y=[0, 0], mode='lines',
                                  line=dict(color=C_IOUT, dash='dash', width=1.2), opacity=0.9,
                                  name='I_min = 0 A'))
    fig.add_vline(x=D * T, line=dict(color=C_GRAY, dash='dot', width=0.8), opacity=0.5)
    fig.add_annotation(x=D * T / 2, y=-0.3, text='D·T', showarrow=False, font=dict(size=8, color=C_GRAY))
    return fig


def build_vi_buck(E, R, D, L, t2='transistor', show_iminmax=False, lang='fr'):
    v_out, i_out_avg, i_in_avg, i_pk, i_lo, _ = buck_solve(E, R, D, L, t2)
    i_max, v_max = VI_I_MAX, VI_V_MAX
    fig = setup_vi_figure(lang, i_max, v_max)
    i_r = np.linspace(0, i_max, 400)
    fig.add_trace(go.Scatter(x=i_r, y=np.clip(i_r * R, 0, v_max), mode='lines',
                              line=dict(color=C_DARK_BLUE, width=1.2), opacity=0.5,
                              name=t('charge_r', lang, R=R)))
    add_operating(fig, i_out=i_out_avg, v_out=v_out, i_in=i_in_avg, v_in=E, avg=True,
                   i_max=i_max, v_max=v_max)
    if show_iminmax:
        p_max = i_pk ** 2 * R
        # i_lo can be negative (transistor CCM) -- clip to visible quadrant
        i_lo_v = max(i_lo, 0.0)
        p_min = i_lo_v ** 2 * R
        fig.add_trace(go.Scatter(x=[min(i_pk, i_max)], y=[min(i_pk * R, v_max)], mode='markers',
                                  marker=dict(symbol='triangle-up', size=11, color=C_ORANGE),
                                  name=f'P_max = {p_max:.1f} W'))
        note = t('out_of_plane', lang) if i_lo < 0 else ''
        fig.add_trace(go.Scatter(x=[i_lo_v], y=[i_lo_v * R], mode='markers',
                                  marker=dict(symbol='triangle-down', size=11, color=C_ORANGE),
                                  name=f'P_min = {p_min:.1f} W{note}'))
    return fig


def build_chrono_buck(E, R, D, L_val, t2='transistor', show_iminmax=False, lang='fr'):
    fig = setup_chrono_figure(lang)
    T_MS = T_S * 1e3
    t_s = np.linspace(0, 2 * T_S, 4000)
    t_ms = t_s * 1e3
    phase_s = t_s % T_S

    v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = buck_solve(E, R, D, L_val, t2)
    slope_up = (E - v_out) / L_val
    slope_dn = v_out / L_val

    if t2 == 'transistor':
        i_L = np.where(phase_s < D * T_S,
                        i_lo + slope_up * phase_s,
                        i_pk - slope_dn * (phase_s - D * T_S))
    elif ccm:
        i_L = np.where(phase_s < D * T_S,
                        i_lo + slope_up * phase_s,
                        i_pk - slope_dn * (phase_s - D * T_S))
        i_L = np.clip(i_L, 0.0, None)
    else:
        t_fall_s = i_pk / slope_dn if slope_dn > 1e-9 else D * T_S
        i_L = np.where(phase_s < D * T_S,
                        slope_up * phase_s,
                        np.where(phase_s < D * T_S + t_fall_s,
                                 i_pk - slope_dn * (phase_s - D * T_S),
                                 0.0))
        i_L = np.clip(i_L, 0.0, None)

    i_in = np.where(phase_s < D * T_S, i_L, 0.0)
    v_out_wave = i_L * R

    fig.add_trace(go.Scatter(x=t_ms, y=v_out_wave, mode='lines', line=dict(color=C_VOUT, width=2),
                              name=f'V_OUT = i_L·R   ⟨⟩={v_out:.2f} V'))
    fig.add_trace(go.Scatter(x=t_ms, y=i_L, mode='lines', line=dict(color=C_IOUT, dash='dash', width=2),
                              name=f'I_OUT = i_L   ⟨⟩={i_out_avg:.2f} A'))
    fig.add_trace(go.Scatter(x=[t_ms[0], t_ms[-1]], y=[E, E], mode='lines',
                              line=dict(color=C_VIN, dash='dot', width=1.8), name=f'V_IN  = {E:.2f} V'))
    fig.add_trace(go.Scatter(x=t_ms, y=i_in, mode='lines', line=dict(color=C_IIN, dash='dashdot', width=2),
                              name=t('iin_pulsed_t1', lang, i_in_avg=i_in_avg)))
    fig.add_hline(y=v_out, line=dict(color=C_VOUT, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=i_out_avg, line=dict(color=C_IOUT, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=i_in_avg, line=dict(color=C_IIN, dash='dot', width=1), opacity=0.55)
    if show_iminmax:
        fig.add_trace(go.Scatter(x=[t_ms[0], t_ms[-1]], y=[i_pk, i_pk], mode='lines',
                                  line=dict(color=C_IOUT, dash='dash', width=1.2), opacity=0.9,
                                  name=f'I_max = {i_pk:.2f} A'))
        fig.add_trace(go.Scatter(x=[t_ms[0], t_ms[-1]], y=[i_lo, i_lo], mode='lines',
                                  line=dict(color=C_IOUT, dash='dash', width=1.2), opacity=0.9,
                                  name=f'I_min = {i_lo:.2f} A'))
    fig.add_vline(x=D * T_MS, line=dict(color=C_GRAY, dash='dot', width=0.8), opacity=0.5)
    fig.add_annotation(x=D * T_MS / 2, y=-0.3, text='D·T', showarrow=False, font=dict(size=8, color=C_GRAY))
    if not ccm:
        fig.add_annotation(text=t('dcm_banner', lang), x=0.5, y=0.75, xref='paper', yref='paper',
                            showarrow=False, font=dict(size=10, color=C_IIN),
                            bgcolor='#fff3e0', bordercolor=C_IIN, borderwidth=1)
    return fig


def build_vi_cap(E, R, D, L, C, t2='transistor', show_iminmax=False, lang='fr'):
    i_L_1p, dt, v_out, i_out_avg, i_in_avg, i_pk, i_lo, _ = buck_i_L_period(E, R, D, L, t2)
    v_ss = cap_vout_ss(i_L_1p, R, C, dt)
    delta_v = np.ptp(v_ss)
    v_hi_raw = np.max(v_ss)
    v_lo = max(np.min(v_ss), 0.0)

    i_max, v_max = VI_I_MAX, VI_V_MAX
    v_hi = min(v_hi_raw, v_max)

    fig = setup_vi_figure(lang, i_max, v_max)
    i_r = np.linspace(0, i_max, 400)
    fig.add_trace(go.Scatter(x=i_r, y=np.clip(i_r * R, 0, v_max), mode='lines',
                              line=dict(color=C_DARK_BLUE, width=1.2), opacity=0.5,
                              name=t('charge_r', lang, R=R)))
    fig.add_trace(go.Scatter(x=[v_lo / R, v_hi / R], y=[v_lo, v_hi], mode='lines',
                              line=dict(color=C_VOUT, width=4), opacity=0.6,
                              name=f'ΔV_pp = {delta_v:.2f} V'))
    add_operating(fig, i_out=i_out_avg, v_out=v_out, i_in=i_in_avg, v_in=E, avg=True,
                   i_max=i_max, v_max=v_max)
    if show_iminmax:
        p_hi = v_hi ** 2 / R
        p_lo = v_lo ** 2 / R
        fig.add_trace(go.Scatter(x=[min(v_hi / R, i_max)], y=[v_hi], mode='markers',
                                  marker=dict(symbol='triangle-up', size=11, color=C_ORANGE),
                                  name=f'P_max = {p_hi:.1f} W'))
        fig.add_trace(go.Scatter(x=[v_lo / R], y=[v_lo], mode='markers',
                                  marker=dict(symbol='triangle-down', size=11, color=C_ORANGE),
                                  name=f'P_min = {p_lo:.1f} W'))
    return fig


def build_chrono_cap(E, R, D, L_val, C, t2='transistor', show_iminmax=False, lang='fr'):
    T_MS = T_S * 1e3
    i_L_1p, dt, v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = buck_i_L_period(E, R, D, L_val, t2)
    v_ss = cap_vout_ss(i_L_1p, R, C, dt)

    i_L = np.tile(i_L_1p, 2)
    v_out_wave = np.tile(v_ss, 2)
    t_ms = np.arange(len(i_L)) * dt * 1e3

    phase_s = (np.arange(len(i_L)) * dt) % T_S
    i_in = np.where(phase_s < D * T_S, i_L, 0.0)
    i_C = i_L - v_out_wave / R   # true capacitor current

    fig = setup_chrono_figure(lang)
    y_min = min(np.min(i_C) - 0.5, -0.5)
    fig.update_layout(yaxis=dict(range=[y_min, CHRONO_Y]))

    fig.add_trace(go.Scatter(x=t_ms, y=v_out_wave, mode='lines', line=dict(color=C_VOUT, width=2),
                              name=f'V_OUT = v̄ + (1/C)∫i_C   ⟨⟩={v_out:.2f} V'))
    fig.add_trace(go.Scatter(x=t_ms, y=i_L, mode='lines', line=dict(color=C_IOUT, dash='dash', width=2),
                              name=f'i_L   ⟨⟩={i_out_avg:.2f} A'))
    fig.add_trace(go.Scatter(x=t_ms, y=i_C, mode='lines', line=dict(color=C_PURPLE, dash='dashdot', width=1.8),
                              name='i_C = i_L - V_OUT/R   ⟨⟩≈0 A'))
    fig.add_trace(go.Scatter(x=[t_ms[0], t_ms[-1]], y=[E, E], mode='lines',
                              line=dict(color=C_VIN, dash='dot', width=1.8), name=f'V_IN = {E:.2f} V'))
    fig.add_trace(go.Scatter(x=t_ms, y=i_in, mode='lines', line=dict(color=C_IIN, dash='dashdot', width=2),
                              name=t('iin_pulsed_t1_lower', lang, i_in_avg=i_in_avg)))

    fig.add_hline(y=v_out, line=dict(color=C_VOUT, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=i_out_avg, line=dict(color=C_IOUT, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=i_in_avg, line=dict(color=C_IIN, dash='dot', width=1), opacity=0.55)
    fig.add_hline(y=0.0, line=dict(color=C_PURPLE, dash='dot', width=0.8), opacity=0.40)

    if show_iminmax:
        fig.add_trace(go.Scatter(x=[t_ms[0], t_ms[-1]], y=[i_pk, i_pk], mode='lines',
                                  line=dict(color=C_IOUT, dash='dash', width=1.2), opacity=0.9,
                                  name=f'I_max = {i_pk:.2f} A'))
        fig.add_trace(go.Scatter(x=[t_ms[0], t_ms[-1]], y=[i_lo, i_lo], mode='lines',
                                  line=dict(color=C_IOUT, dash='dash', width=1.2), opacity=0.9,
                                  name=f'I_min = {i_lo:.2f} A'))

    fig.add_vline(x=D * T_MS, line=dict(color=C_GRAY, dash='dot', width=0.8), opacity=0.5)
    fig.add_annotation(x=D * T_MS / 2, y=y_min + 0.2, text='D·T', showarrow=False,
                        font=dict(size=8, color=C_GRAY))
    if not ccm:
        fig.add_annotation(text=t('dcm_banner', lang), x=0.5, y=0.75, xref='paper', yref='paper',
                            showarrow=False, font=dict(size=10, color=C_IIN),
                            bgcolor='#fff3e0', bordercolor=C_IIN, borderwidth=1)
    return fig


def register_plot_callback(app):
    @app.callback(
        Output('circuit-img', 'src'),
        Output('vi-plane-graph', 'figure'),
        Output('chrono-graph', 'figure'),
        Input('mode-select', 'value'),
        Input('t2-select', 'value'),
        Input('show-iminmax', 'value'),
        Input('slider-E', 'value'),
        Input('slider-R', 'value'),
        Input('slider-Rth', 'value'),
        Input('slider-D', 'value'),
        Input('slider-L', 'value'),
        Input('slider-C', 'value'),
        Input('lang-store', 'data'),
    )
    def update_plots(mode, t2, show_iminmax_val, E, r_log, rth_log, D, l_log, c_log, lang):
        R = 10 ** r_log
        Rth = 10 ** rth_log
        L = 10 ** l_log
        C = 10 ** c_log
        show_iminmax = bool(show_iminmax_val)
        lang = lang or 'fr'

        if mode == 'direct':
            vi_fig = build_vi_direct(E, R, lang)
            chrono_fig = build_chrono_direct(E, R, lang)
        elif mode == 'rth':
            vi_fig = build_vi_rth(E, R, Rth, lang)
            chrono_fig = build_chrono_rth(E, R, Rth, lang)
        elif mode == 'switch':
            vi_fig = build_vi_switch(E, R, D, show_iminmax, lang)
            chrono_fig = build_chrono_switch(E, R, D, show_iminmax, lang)
        elif mode == 'buck':
            vi_fig = build_vi_buck(E, R, D, L, t2, show_iminmax, lang)
            chrono_fig = build_chrono_buck(E, R, D, L, t2, show_iminmax, lang)
        else:  # cap
            vi_fig = build_vi_cap(E, R, D, L, C, t2, show_iminmax, lang)
            chrono_fig = build_chrono_cap(E, R, D, L, C, t2, show_iminmax, lang)

        img_src = _circuit_img_src(mode, t2)
        return img_src, vi_fig, chrono_fig
