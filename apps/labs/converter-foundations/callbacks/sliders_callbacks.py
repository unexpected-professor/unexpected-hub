from dash.dependencies import Input, Output

_SHOW = {'display': 'block'}
_HIDE = {'display': 'none'}


def register_slider_callbacks(app):
    @app.callback(
        Output('div-Rth', 'style'),
        Output('div-D', 'style'),
        Output('div-L', 'style'),
        Output('div-C', 'style'),
        Output('div-imm', 'style'),
        Output('div-t2', 'style'),
        Input('mode-select', 'value'),
    )
    def toggle_controls(mode):
        return (
            _SHOW if mode == 'rth' else _HIDE,
            _SHOW if mode in ('switch', 'buck', 'cap') else _HIDE,
            _SHOW if mode in ('buck', 'cap') else _HIDE,
            _SHOW if mode == 'cap' else _HIDE,
            _SHOW if mode in ('switch', 'buck', 'cap') else _HIDE,
            _SHOW if mode in ('buck', 'cap') else _HIDE,
        )

    @app.callback(
        Output('col-vi', 'style'),
        Output('col-chrono', 'style'),
        Input('panel-visibility', 'value'),
    )
    def toggle_panels(panels):
        panels = panels or []
        return (
            _SHOW if 'vi' in panels else _HIDE,
            _SHOW if 'chrono' in panels else _HIDE,
        )
