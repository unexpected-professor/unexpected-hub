"""Shared, tool-agnostic layout building blocks: the collapsible 3-pane shell and the
slider+editable-input widgets. Used by both layouts/main_layout.py (CM1) and
layouts/cm2_layout.py (CM2).
"""

import numpy as np
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from i18n import t

LEFT_PANE_WIDTH = '320px'
RIGHT_PANE_WIDTH = '280px'

# paddingTop clears the toggle-handle buttons, which sit on the same flex row at the top of
# the page (otherwise the first line of pane content renders right beside/over the button).
LEFT_PANE_STYLE = {'flex': f'0 0 {LEFT_PANE_WIDTH}', 'paddingTop': '2rem'}
RIGHT_PANE_STYLE = {'flex': f'0 0 {RIGHT_PANE_WIDTH}', 'paddingTop': '2rem'}
HIDDEN_PANE_STYLE = {'display': 'none'}

# Vertical-divider handles sit between the panes and always stay visible (even when the
# pane they control is hidden), so the pane can always be re-expanded.
_HANDLE_BASE_STYLE = {
    'display': 'flex', 'alignItems': 'flex-start', 'justifyContent': 'center',
    'paddingTop': '0.25rem', 'alignSelf': 'stretch',
}
LEFT_HANDLE_STYLE = {**_HANDLE_BASE_STYLE, 'borderRight': '1px solid #dee2e6',
                      'paddingRight': '0.5rem', 'marginRight': '0.75rem'}
RIGHT_HANDLE_STYLE = {**_HANDLE_BASE_STYLE, 'borderLeft': '1px solid #dee2e6',
                      'paddingLeft': '0.5rem', 'marginLeft': '0.75rem'}

# Uniform button size regardless of label length, matching the original mockup request.
MODE_LABEL_STYLE = {'height': '44px', 'display': 'flex', 'alignItems': 'center'}

INPUT_TEXT_STYLE = {'textAlign': 'left'}


def linear_slider_with_input(slider_id, input_id, label, vmin, vmax, value, unit=None, step=None,
                              label_id=None):
    input_ctrl = dbc.Input(id=input_id, type='number', value=value, size='sm', style=INPUT_TEXT_STYLE)
    if unit:
        input_ctrl = dbc.InputGroup([input_ctrl, dbc.InputGroupText(unit)], size='sm')
    return html.Div([
        dbc.Label(label, html_for=slider_id, id=label_id) if label_id else dbc.Label(label, html_for=slider_id),
        dcc.Slider(id=slider_id, min=vmin, max=vmax, step=step, value=value, marks={}, updatemode='drag'),
        html.Div(input_ctrl, className='mt-1'),
    ])


def log_slider_with_input(slider_id, input_id, label, unit, exp_min, exp_max, value,
                           unit_scale=1.0, n_marks=5, value_fmt='{:.3g}', label_id=None):
    marks = {
        round(float(exp), 4): value_fmt.format((10 ** exp) * unit_scale)
        for exp in np.linspace(exp_min, exp_max, n_marks)
    }
    real_init = round((10 ** value) * unit_scale, 6)
    return html.Div([
        dbc.Label(label, html_for=slider_id, id=label_id) if label_id else dbc.Label(label, html_for=slider_id),
        dcc.Slider(id=slider_id, min=exp_min, max=exp_max, step=0.01, value=value,
                   marks=marks, updatemode='drag'),
        dbc.InputGroup([
            dbc.Input(id=input_id, type='number', value=real_init, size='sm', style=INPUT_TEXT_STYLE),
            dbc.InputGroupText(unit),
        ], size='sm', className='mt-1'),
    ])


def three_pane_shell(left_content, center_content, right_content,
                      left_pane_id, center_pane_id, right_pane_id,
                      toggle_left_id, toggle_right_id):
    """The collapsible left-controls / center-graphs / right-sliders layout, with the
    pane-toggle buttons living in bordered "handle" divs at the seams so they stay visible
    (and clickable) even when their pane is hidden."""
    return html.Div([
        html.Div(left_content, id=left_pane_id, style=LEFT_PANE_STYLE),
        html.Div(dbc.Button('◂', id=toggle_left_id, size='sm', outline=True, color='secondary',
                             className='px-1 py-0'), style=LEFT_HANDLE_STYLE),
        dbc.Tooltip(t('tt_pane_toggle'), target=toggle_left_id, placement='auto', id=f'tt-{toggle_left_id}'),
        html.Div(center_content, id=center_pane_id, style={'flex': '1 1 auto', 'minWidth': 0}),
        html.Div(dbc.Button('▸', id=toggle_right_id, size='sm', outline=True, color='secondary',
                             className='px-1 py-0'), style=RIGHT_HANDLE_STYLE),
        dbc.Tooltip(t('tt_pane_toggle'), target=toggle_right_id, placement='auto', id=f'tt-{toggle_right_id}'),
        html.Div(right_content, id=right_pane_id, style=RIGHT_PANE_STYLE),
    ], style={'display': 'flex', 'alignItems': 'flex-start'})
