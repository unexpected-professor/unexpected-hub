"""Shared, topology-agnostic V-I plane / chronogram figure builders.

Used by both `plots_callback.py` and `cm2_plots_callback.py` — none of this code
depends on which converter topology is being demonstrated, only on the numeric
operating-point values passed in.
"""

import plotly.graph_objects as go

from models.converter_physics import VI_I_MAX, VI_V_MAX, CHRONO_Y, iso_power_grid
from i18n import t

C_GREEN = '#2a7a3d'
C_RED = '#ae3d25'
C_BLUE = '#143d7a'
C_ORANGE = '#e07b00'
C_GRAY = '#585858'
C_ISO = '#cccccc'
C_DARK_BLUE = '#0C21E4'
C_PURPLE = '#AB04CC'

# Colour/quantity convention: V_OUT green, I_OUT red, V_IN blue, I_IN orange
C_VOUT, C_IOUT, C_VIN, C_IIN = C_GREEN, C_RED, C_BLUE, C_ORANGE

STATIC_ISO_POWERS = [1, 10, 100]


def setup_vi_figure(lang='fr', i_max=VI_I_MAX, v_max=VI_V_MAX):
    fig = go.Figure()
    for entry in iso_power_grid(i_max=i_max, v_max=v_max, powers=STATIC_ISO_POWERS):
        fig.add_trace(go.Scatter(
            x=entry['i'], y=entry['v'], mode='lines',
            line=dict(color=C_ISO, dash='dash', width=entry['lw']),
            opacity=0.85, showlegend=False, hoverinfo='skip',
        ))
        if entry['label_pos']:
            il, vl = entry['label_pos']
            fig.add_annotation(x=il, y=vl, text=f"{entry['P']}W", showarrow=False,
                                font=dict(size=9, color=C_GRAY), textangle=45,
                                bgcolor='white')
    fig.update_layout(
        xaxis=dict(title=t('axis_current', lang), range=[0, i_max], gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title=t('axis_voltage', lang), range=[0, v_max], gridcolor='rgba(0,0,0,0.1)'),
        title=t('vi_title', lang),
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=50, r=20, t=40, b=40),
        legend=dict(x=0.98, y=0.98, xanchor='right', yanchor='top', font=dict(size=10)),
    )
    return fig


def setup_chrono_figure(lang='fr', y_range=(-0.5, CHRONO_Y), x_title=None, y_title=None):
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(title=x_title or t('axis_time', lang), range=[0, 2], gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title=y_title or t('axis_chrono_y', lang), range=list(y_range),
                   gridcolor='rgba(0,0,0,0.1)'),
        title=t('chrono_title', lang),
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=50, r=20, t=40, b=40),
        legend=dict(x=0.98, y=0.98, xanchor='right', yanchor='top', font=dict(size=10)),
    )
    return fig


def add_power_curves(fig, i_out, v_out, i_in, v_in, i_max, v_max):
    """Two iso-power hyperbolas tracking the instantaneous source (V_IN*I_IN, at the input
    operating point) and load (V_OUT*I_OUT, at the output operating point), recomputed every
    time the parameters change — unlike the static 1/10/100 W reference grid. In a lossless
    conversion the two coincide and render as a single curve, visually showing power is
    conserved through the converter. Each curve's tag is anchored (with a short leader line)
    directly at its own operating-point marker rather than at an arbitrary point along the
    curve, so the tag stays next to what it's describing instead of floating elsewhere on
    the plot — using opposite arrow offsets keeps the two tags apart even in the direct-mode
    case where both markers coincide at the same (i, v) point."""
    p_source = v_in * i_in
    p_load = v_out * i_out
    src_entry, load_entry = iso_power_grid(i_max=i_max, v_max=v_max, powers=[p_source, p_load])
    fig.add_trace(go.Scatter(x=src_entry['i'], y=src_entry['v'], mode='lines',
                              line=dict(color=C_IIN, dash='dot', width=2), opacity=0.9,
                              name=f'P_source = {p_source:.1f} W', showlegend=False))
    fig.add_trace(go.Scatter(x=load_entry['i'], y=load_entry['v'], mode='lines',
                              line=dict(color=C_VOUT, dash='dot', width=2), opacity=0.9,
                              name=f'P_load = {p_load:.1f} W', showlegend=False))

    fig.add_annotation(x=i_in, y=v_in, text=f'P_source = {p_source:.1f} W',
                        showarrow=True, arrowhead=2, arrowcolor=C_IIN, ax=45, ay=-35,
                        font=dict(size=10, color=C_IIN),
                        bgcolor='rgba(255,255,255,0.9)', bordercolor=C_IIN, borderwidth=1)
    fig.add_annotation(x=i_out, y=v_out, text=f'P_load = {p_load:.1f} W',
                        showarrow=True, arrowhead=2, arrowcolor=C_VOUT, ax=-45, ay=35,
                        font=dict(size=10, color=C_VOUT),
                        bgcolor='rgba(255,255,255,0.9)', bordercolor=C_VOUT, borderwidth=1)


def add_operating(fig, i_out, v_out, i_in, v_in, avg=False, i_max=VI_I_MAX, v_max=VI_V_MAX):
    """Crosshairs + markers for output and input operating points on the V-I plane, plus the
    dynamic source/load power-tracking curves."""
    def wrap(s):
        return f'⟨{s}⟩' if avg else s

    fig.add_trace(go.Scatter(x=[0, i_max], y=[v_out, v_out], mode='lines',
                              line=dict(color=C_VOUT, dash='dash', width=1), opacity=0.65,
                              name=f'{wrap("V_OUT")} = {v_out:.2f} V'))
    fig.add_trace(go.Scatter(x=[i_out, i_out], y=[0, v_max], mode='lines',
                              line=dict(color=C_IOUT, dash='dash', width=1), opacity=0.65,
                              name=f'{wrap("I_OUT")} = {i_out:.2f} A'))
    fig.add_trace(go.Scatter(x=[0, i_max], y=[v_in, v_in], mode='lines',
                              line=dict(color=C_VIN, dash='dot', width=1), opacity=0.65,
                              name=f'{wrap("V_IN")}  = {v_in:.2f} V'))
    fig.add_trace(go.Scatter(x=[i_in, i_in], y=[0, v_max], mode='lines',
                              line=dict(color=C_IIN, dash='dashdot', width=1), opacity=0.65,
                              name=f'{wrap("I_IN")}  = {i_in:.2f} A'))
    fig.add_trace(go.Scatter(x=[i_out], y=[v_out], mode='markers',
                              marker=dict(symbol='circle', size=14, color=C_VOUT), showlegend=False))
    fig.add_trace(go.Scatter(x=[i_in], y=[v_in], mode='markers',
                              marker=dict(symbol='square', size=12, color=C_VIN), showlegend=False))
    add_power_curves(fig, i_out=i_out, v_out=v_out, i_in=i_in, v_in=v_in, i_max=i_max, v_max=v_max)
