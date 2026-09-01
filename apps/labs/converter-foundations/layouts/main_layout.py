import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc

from models.converter_physics import INIT
from i18n import TEXT, t
from layouts.widgets import (
    linear_slider_with_input, log_slider_with_input, three_pane_shell, MODE_LABEL_STYLE,
)

GRAPH_CONFIG = {'responsive': True}

MODE_OPTIONS = [
    {'label': t('mode_direct'), 'value': 'direct'},
    {'label': t('mode_rth'), 'value': 'rth'},
    {'label': t('mode_switch'), 'value': 'switch'},
    {'label': t('mode_buck'), 'value': 'buck'},
    {'label': t('mode_cap'), 'value': 'cap'},
]

left_pane_content = [
    html.H6(t('circuit_view'), id='circuit-view-title', className='mt-2'),
    html.Img(id='circuit-img', style={'width': '100%'}),
    html.Hr(),
    html.H6(t('cas'), id='cas-title', className='mt-2'),
    html.Div(
        dbc.RadioItems(
            id='mode-select',
            options=MODE_OPTIONS,
            value='direct',
            input_class_name='btn-check',
            label_class_name='btn btn-outline-primary text-start',
            label_checked_class_name='active',
            label_style=MODE_LABEL_STYLE,
        ),
        className='d-grid gap-2 mb-3',
    ),
    dbc.Tooltip(t('tt_mode_select'), target='mode-select', placement='auto', id='tt-mode-select'),
    html.Hr(),
    html.H6(t('affichage'), id='affichage-title'),
    dbc.Checklist(
        id='panel-visibility',
        options=[
            {'label': t('plan_vi'), 'value': 'vi'},
            {'label': t('chrono_label'), 'value': 'chrono'},
        ],
        value=['vi', 'chrono'],
        switch=True,
        input_style={'marginLeft': '0'},
        className='mb-3',
    ),
    dbc.Tooltip(t('tt_panel_visibility'), target='panel-visibility', placement='auto', id='tt-panel-visibility'),
    html.Div(
        dbc.Checklist(
            id='show-iminmax',
            options=[{'label': 'I · P max/min', 'value': 'on'}],
            value=['on'],
            switch=True,
            input_style={'marginLeft': '0'},
        ),
        id='div-imm',
        className='mb-3',
    ),
    dbc.Tooltip(t('tt_show_iminmax'), target='div-imm', placement='auto', id='tt-show-iminmax'),
    html.Div([
        html.Hr(),
        html.Div('Buck T₂', className='text-muted small mb-1'),
        dbc.RadioItems(
            id='t2-select',
            options=[
                {'label': 'MOSFET', 'value': 'transistor'},
                {'label': 'Diode', 'value': 'diode'},
            ],
            value='diode',
            input_class_name='btn-check',
            label_class_name='btn btn-outline-primary btn-sm',
            label_checked_class_name='active',
            inline=True,
        ),
    ], id='div-t2'),
    dbc.Tooltip(t('tt_switch_select'), target='t2-select', placement='auto', id='tt-t2-select'),
]

# Graphs sit side by side only when there is real room (>= 1400 px: the lab
# open full-screen on a wide display); otherwise they stack.
center_pane_content = dbc.Row([
    dbc.Col(dcc.Graph(id='vi-plane-graph', style={'height': '62vh'}, config=GRAPH_CONFIG),
            xs=12, xxl=6, id='col-vi'),
    dbc.Col(dcc.Graph(id='chrono-graph', style={'height': '62vh'}, config=GRAPH_CONFIG),
            xs=12, xxl=6, id='col-chrono'),
])

right_pane_content = [
    html.H6(t('parameters'), id='parameters-title', className='mt-2 mb-3'),
    linear_slider_with_input('slider-E', 'input-E', 'E (V)', 1.0, 24.0, INIT['E'], unit='V', step=0.5),
    dbc.Tooltip(t('tt_slider_E'), target='slider-E', placement='auto', id='tt-slider-E'),
    html.Div(
        log_slider_with_input('slider-R', 'input-R', 'R (Ω)', 'Ω', -1.0, 1.0, float(np.log10(INIT['R']))),
        className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_R'), target='slider-R', placement='auto', id='tt-slider-R'),
    html.Div(
        log_slider_with_input('slider-Rth', 'input-Rth', 'Rth (Ω)', 'Ω', -1.0, 1.0, float(np.log10(INIT['Rth']))),
        id='div-Rth', className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_Rth'), target='div-Rth', placement='auto', id='tt-slider-Rth'),
    html.Div(
        linear_slider_with_input('slider-D', 'input-D', 'D', 0.05, 0.95, INIT['D'], step=0.05),
        id='div-D', className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_D'), target='div-D', placement='auto', id='tt-slider-D'),
    html.Div(
        log_slider_with_input('slider-L', 'input-L', 'L (µH)', 'µH', -4.0, -3.0, float(np.log10(INIT['L'])),
                               unit_scale=1e6, n_marks=3, value_fmt='{:.0f}'),
        id='div-L', className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_L'), target='div-L', placement='auto', id='tt-slider-L'),
    html.Div(
        log_slider_with_input('slider-C', 'input-C', 'C (µF)', 'µF', -6.0, -2.0, float(np.log10(INIT['C'])),
                               unit_scale=1e6, n_marks=5, value_fmt='{:.0f}'),
        id='div-C', className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_C'), target='div-C', placement='auto', id='tt-slider-C'),
]

header = html.H4(TEXT['title']['fr'], id='app-title', className='mt-3 mb-3')

cm1_layout = dbc.Container([
    dcc.Store(id='left-collapsed-store', data=False),
    dcc.Store(id='right-collapsed-store', data=False),
    header,
    three_pane_shell(
        left_pane_content, center_pane_content, right_pane_content,
        left_pane_id='left-pane', center_pane_id='center-pane', right_pane_id='right-pane',
        toggle_left_id='toggle-left-btn', toggle_right_id='toggle-right-btn',
    ),
], fluid=True)
