from dash.dependencies import Input, Output, State

from layouts.widgets import LEFT_PANE_STYLE, RIGHT_PANE_STYLE, HIDDEN_PANE_STYLE


def _register_pane_toggles(app, left_pane_id, right_pane_id, left_store_id, right_store_id,
                            toggle_left_id, toggle_right_id):
    @app.callback(
        Output(left_store_id, 'data'),
        Input(toggle_left_id, 'n_clicks'),
        State(left_store_id, 'data'),
        prevent_initial_call=True,
    )
    def toggle_left(_n_clicks, collapsed):
        return not collapsed

    @app.callback(
        Output(left_pane_id, 'style'),
        Output(toggle_left_id, 'children'),
        Input(left_store_id, 'data'),
    )
    def apply_left(collapsed):
        return (HIDDEN_PANE_STYLE, '▸') if collapsed else (LEFT_PANE_STYLE, '◂')

    @app.callback(
        Output(right_store_id, 'data'),
        Input(toggle_right_id, 'n_clicks'),
        State(right_store_id, 'data'),
        prevent_initial_call=True,
    )
    def toggle_right(_n_clicks, collapsed):
        return not collapsed

    @app.callback(
        Output(right_pane_id, 'style'),
        Output(toggle_right_id, 'children'),
        Input(right_store_id, 'data'),
    )
    def apply_right(collapsed):
        return (HIDDEN_PANE_STYLE, '◂') if collapsed else (RIGHT_PANE_STYLE, '▸')


def register_layout_callbacks(app):
    _register_pane_toggles(app, 'left-pane', 'right-pane',
                            'left-collapsed-store', 'right-collapsed-store',
                            'toggle-left-btn', 'toggle-right-btn')
    _register_pane_toggles(app, 'cm2-left-pane', 'cm2-right-pane',
                            'cm2-left-collapsed-store', 'cm2-right-collapsed-store',
                            'cm2-toggle-left-btn', 'cm2-toggle-right-btn')


def register_tab_switch_callback(app):
    """cm-tabs is a slim selector with no `children` payload (see app.py) — this callback
    shows/hides the actual CM1/CM2 page divs, which live outside the Tabs component entirely."""
    @app.callback(
        Output('cm1-page', 'style'),
        Output('cm2-page', 'style'),
        Input('cm-tabs', 'value'),
    )
    def switch_tab(tab):
        return (
            {} if tab == 'cm1' else HIDDEN_PANE_STYLE,
            {} if tab == 'cm2' else HIDDEN_PANE_STYLE,
        )
