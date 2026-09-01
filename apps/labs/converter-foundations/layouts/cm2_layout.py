import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc

from models.cm2_physics import INIT
from i18n import t
from layouts.widgets import (
    linear_slider_with_input, log_slider_with_input, three_pane_shell, MODE_LABEL_STYLE,
)

GRAPH_CONFIG = {'responsive': True}

MODE_OPTIONS = [
    {'label': t('mode_buck2'), 'value': 'buck'},
    {'label': t('mode_boost2'), 'value': 'boost'},
]

cm2_left_pane_content = [
    html.H6(t('circuit_view'), id='cm2-circuit-view-title', className='mt-2'),
    html.Img(id='cm2-circuit-img', style={'width': '100%'}),
    html.Hr(),
    html.H6(t('cas'), id='cm2-cas-title', className='mt-2'),
    html.Div(
        dbc.RadioItems(
            id='cm2-mode-select',
            options=MODE_OPTIONS,
            value='buck',
            input_class_name='btn-check',
            label_class_name='btn btn-outline-primary text-start',
            label_checked_class_name='active',
            label_style=MODE_LABEL_STYLE,
        ),
        className='d-grid gap-2 mb-3',
    ),
    dbc.Tooltip(t('tt_mode_select2'), target='cm2-mode-select', placement='auto', id='tt-cm2-mode-select'),
    html.Hr(),
    html.H6(t('affichage'), id='cm2-affichage-title'),
    dbc.Checklist(
        id='cm2-panel-visibility',
        options=[
            {'label': t('plan_vi'), 'value': 'vi'},
            {'label': t('chrono_label'), 'value': 'chrono'},
            {'label': t('voutd_label'), 'value': 'voutd'},
        ],
        value=['vi', 'chrono', 'voutd'],
        switch=True,
        input_style={'marginLeft': '0'},
        className='mb-3',
    ),
    dbc.Tooltip(t('tt_panel_visibility'), target='cm2-panel-visibility', placement='auto',
                id='tt-cm2-panel-visibility'),
    dbc.Checklist(
        id='cm2-show-dcmzone',
        options=[{'label': t('dcm_zone_label'), 'value': 'on'}],
        value=['on'],
        switch=True,
        input_style={'marginLeft': '0'},
        className='mb-3',
    ),
    dbc.Tooltip(t('tt_show_dcmzone'), target='cm2-show-dcmzone', placement='auto', id='tt-cm2-show-dcmzone'),
    dbc.Checklist(
        id='cm2-show-iminmax',
        options=[{'label': 'I · P max/min', 'value': 'on'}],
        value=['on'],
        switch=True,
        input_style={'marginLeft': '0'},
        className='mb-3',
    ),
    dbc.Tooltip(t('tt_show_iminmax'), target='cm2-show-iminmax', placement='auto', id='tt-cm2-show-iminmax'),
    html.Hr(),
    html.H6(t('switch_label'), id='cm2-switch-title'),
    dbc.RadioItems(
        id='cm2-t2-select',
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
    dbc.Tooltip(t('tt_switch_select'), target='cm2-t2-select', placement='auto', id='tt-cm2-t2-select'),
]

cm2_center_pane_content = html.Div([
    dbc.Row([
        dbc.Col(dcc.Graph(id='cm2-vi-plane-graph', style={'height': '45vh'}, config=GRAPH_CONFIG),
                xs=12, xxl=6, id='cm2-col-vi'),
        dbc.Col(dcc.Graph(id='cm2-chrono-graph', style={'height': '45vh'}, config=GRAPH_CONFIG),
                xs=12, xxl=6, id='cm2-col-chrono'),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='cm2-voutd-graph', style={'height': '28vh'}, config=GRAPH_CONFIG),
                width=12, id='cm2-col-voutd'),
    ], className='mt-3'),
])

cm2_right_pane_content = [
    html.H6(t('parameters'), id='cm2-parameters-title', className='mt-2 mb-3'),
    linear_slider_with_input('cm2-slider-E', 'cm2-input-E', 'E (V)', 1.0, 24.0, INIT['E'], unit='V', step=0.5),
    dbc.Tooltip(t('tt_slider_E'), target='cm2-slider-E', placement='auto', id='tt-cm2-slider-E'),
    html.Div(
        log_slider_with_input('cm2-slider-R', 'cm2-input-R', 'R (Ω)', 'Ω', -1.0, 2.0,
                               float(np.log10(INIT['R'])), n_marks=4),
        className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_R'), target='cm2-slider-R', placement='auto', id='tt-cm2-slider-R'),
    html.Div(
        linear_slider_with_input('cm2-slider-D', 'cm2-input-D', 'D', 0.05, 0.95, INIT['D'], step=0.05),
        className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_D'), target='cm2-slider-D', placement='auto', id='tt-cm2-slider-D'),
    html.Div(
        log_slider_with_input('cm2-slider-L', 'cm2-input-L', 'L (µH)', 'µH', -5.0, -2.0,
                               float(np.log10(INIT['L'])), unit_scale=1e6, n_marks=4, value_fmt='{:.0f}'),
        className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_L'), target='cm2-slider-L', placement='auto', id='tt-cm2-slider-L'),
    html.Div(
        log_slider_with_input('cm2-slider-F', 'cm2-input-F', 'f (kHz)', 'kHz', 2.0, 5.0,
                               float(np.log10(INIT['F'])), unit_scale=1e-3, n_marks=4, value_fmt='{:.3g}'),
        className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_F'), target='cm2-slider-F', placement='auto', id='tt-cm2-slider-F'),
    html.Div(
        log_slider_with_input('cm2-slider-C', 'cm2-input-C', 'C_low (µF)', 'µF', -6.0, -2.0,
                               float(np.log10(INIT['C'])), unit_scale=1e6, n_marks=5, value_fmt='{:.0f}',
                               label_id='cm2-c-label'),
        className='mt-3',
    ),
    dbc.Tooltip(t('tt_slider_C'), target='cm2-slider-C', placement='auto', id='tt-cm2-slider-C'),
]

cm2_layout = dbc.Container([
    dcc.Store(id='cm2-left-collapsed-store', data=False),
    dcc.Store(id='cm2-right-collapsed-store', data=False),
    html.H4(t('title2'), id='cm2-app-title', className='mt-3 mb-3'),
    three_pane_shell(
        cm2_left_pane_content, cm2_center_pane_content, cm2_right_pane_content,
        left_pane_id='cm2-left-pane', center_pane_id='cm2-center-pane', right_pane_id='cm2-right-pane',
        toggle_left_id='cm2-toggle-left-btn', toggle_right_id='cm2-toggle-right-btn',
    ),
], fluid=True)
