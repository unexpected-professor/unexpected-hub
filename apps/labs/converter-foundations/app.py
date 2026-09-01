"""Converter Foundations — interactive laboratory (The Unexpected Professor).

Dash application demonstrating power-conversion fundamentals and continuous /
discontinuous conduction for Buck and Boost converters.

Development:   python app.py           (debug is OFF unless DASH_DEBUG=1)
Production:    gunicorn app:server -c gunicorn.conf.py

Adapted from the author's existing power-electronics teaching materials.
"""

import os

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from layouts.main_layout import cm1_layout
from layouts.cm2_layout import cm2_layout
from callbacks.sliders_callbacks import register_slider_callbacks
from callbacks.cm2_sliders_callbacks import register_cm2_slider_callbacks
from callbacks.plots_callback import register_plot_callback
from callbacks.cm2_plots_callback import register_cm2_plot_callback
from callbacks.layout_callbacks import register_layout_callbacks, register_tab_switch_callback
from callbacks.value_sync_callbacks import (
    register_value_sync_callbacks, register_cm2_value_sync_callbacks, register_switch_sync_callback,
)
from callbacks.i18n_callbacks import register_i18n_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Fondamentaux de la conversion — The Unexpected Professor'

# The WSGI entry point used by Gunicorn in production.
server = app.server


@server.route('/healthz')
def healthz():
    """Liveness probe. Reveals no configuration."""
    return 'ok', 200, {'Content-Type': 'text/plain; charset=utf-8'}


top_right_controls = html.Div(
    dbc.Button('EN', id='lang-toggle-btn', size='sm', outline=True, color='secondary'),
    style={'position': 'absolute', 'top': '0.5rem', 'right': '1rem', 'zIndex': 10},
)

# dcc.Tabs is used purely as a slim selector (no `children` payload) so its own `style` can be
# freely narrowed/positioned without any risk to page content — the two topic layouts are
# separate, plain html.Div siblings toggled by a callback on cm-tabs' value.
tabs_bar = dcc.Tabs(id='cm-tabs', value='cm1', style={'width': 'fit-content'}, children=[
    dcc.Tab(label='Fondamentaux', value='cm1'),
    dcc.Tab(label='Conduction CCM / DCM', value='cm2'),
])

app.layout = dbc.Container([
    dcc.Store(id='lang-store', data='fr'),
    html.Div([tabs_bar, top_right_controls], style={'position': 'relative'}, className='mt-2'),
    html.Div(cm1_layout, id='cm1-page'),
    html.Div(cm2_layout, id='cm2-page', style={'display': 'none'}),
    dbc.Tooltip('Change language', target='lang-toggle-btn', placement='bottom', id='tt-lang-toggle'),
], fluid=True)

register_slider_callbacks(app)
register_cm2_slider_callbacks(app)
register_plot_callback(app)
register_cm2_plot_callback(app)
register_layout_callbacks(app)
register_tab_switch_callback(app)
register_value_sync_callbacks(app)
register_cm2_value_sync_callbacks(app)
register_switch_sync_callback(app)
register_i18n_callbacks(app)

if __name__ == '__main__':
    # Debug mode is opt-in and never the default, so a production process that
    # merely runs this module cannot expose it.
    debug = os.environ.get('DASH_DEBUG') == '1'
    app.run(debug=debug, host='127.0.0.1', port=int(os.environ.get('PORT', '8050')))
