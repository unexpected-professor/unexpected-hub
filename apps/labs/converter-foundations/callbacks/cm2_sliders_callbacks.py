from dash.dependencies import Input, Output

_SHOW = {'display': 'block'}
_HIDE = {'display': 'none'}


def register_cm2_slider_callbacks(app):
    @app.callback(
        Output('cm2-col-vi', 'style'),
        Output('cm2-col-chrono', 'style'),
        Output('cm2-col-voutd', 'style'),
        Input('cm2-panel-visibility', 'value'),
    )
    def toggle_panels(panels):
        panels = panels or []
        return (
            _SHOW if 'vi' in panels else _HIDE,
            _SHOW if 'chrono' in panels else _HIDE,
            _SHOW if 'voutd' in panels else _HIDE,
        )

    @app.callback(Output('cm2-c-label', 'children'), Input('cm2-mode-select', 'value'))
    def update_c_label(mode):
        return 'C_low (µF)' if mode == 'buck' else 'C_high (µF)'
