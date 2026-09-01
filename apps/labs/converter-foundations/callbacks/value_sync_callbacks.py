import numpy as np
from dash import ctx
from dash.dependencies import Input, Output


def _register_linear_sync(app, slider_id, input_id, vmin, vmax):
    @app.callback(
        Output(slider_id, 'value'),
        Output(input_id, 'value'),
        Input(slider_id, 'value'),
        Input(input_id, 'value'),
        prevent_initial_call=True,
    )
    def sync(slider_val, input_val):
        if ctx.triggered_id == input_id and input_val is not None:
            v = float(np.clip(input_val, vmin, vmax))
            return v, v
        return slider_val, slider_val


def _register_log_sync(app, slider_id, input_id, exp_min, exp_max, unit_scale=1.0):
    real_min = (10 ** exp_min) * unit_scale
    real_max = (10 ** exp_max) * unit_scale

    @app.callback(
        Output(slider_id, 'value'),
        Output(input_id, 'value'),
        Input(slider_id, 'value'),
        Input(input_id, 'value'),
        prevent_initial_call=True,
    )
    def sync(slider_log, input_real):
        if ctx.triggered_id == input_id and input_real is not None:
            real = float(np.clip(input_real, real_min, real_max))
            log_val = float(np.clip(np.log10(real / unit_scale), exp_min, exp_max))
            return log_val, round((10 ** log_val) * unit_scale, 6)
        return slider_log, round((10 ** slider_log) * unit_scale, 6)


def register_value_sync_callbacks(app):
    _register_linear_sync(app, 'slider-E', 'input-E', 1.0, 24.0)
    _register_linear_sync(app, 'slider-D', 'input-D', 0.05, 0.95)
    _register_log_sync(app, 'slider-R', 'input-R', -1.0, 1.0)
    _register_log_sync(app, 'slider-Rth', 'input-Rth', -1.0, 1.0)
    _register_log_sync(app, 'slider-L', 'input-L', -4.0, -3.0, unit_scale=1e6)
    _register_log_sync(app, 'slider-C', 'input-C', -6.0, -2.0, unit_scale=1e6)


def register_cm2_value_sync_callbacks(app):
    _register_linear_sync(app, 'cm2-slider-E', 'cm2-input-E', 1.0, 24.0)
    _register_linear_sync(app, 'cm2-slider-D', 'cm2-input-D', 0.05, 0.95)
    _register_log_sync(app, 'cm2-slider-R', 'cm2-input-R', -1.0, 2.0)
    _register_log_sync(app, 'cm2-slider-L', 'cm2-input-L', -5.0, -2.0, unit_scale=1e6)
    _register_log_sync(app, 'cm2-slider-F', 'cm2-input-F', 2.0, 5.0, unit_scale=1e-3)
    _register_log_sync(app, 'cm2-slider-C', 'cm2-input-C', -6.0, -2.0, unit_scale=1e6)


def register_switch_sync_callback(app):
    """CM1's t2-select and CM2's cm2-t2-select are two separate controls (each positioned and
    conditionally shown within its own tab) that represent one shared MOSFET/Diode choice —
    keeps them mirrored so they always agree, regardless of which one the user touches."""
    @app.callback(
        Output('t2-select', 'value'),
        Output('cm2-t2-select', 'value'),
        Input('t2-select', 'value'),
        Input('cm2-t2-select', 'value'),
        prevent_initial_call=True,
    )
    def sync(v1, v2):
        if ctx.triggered_id == 'cm2-t2-select':
            return v2, v2
        return v1, v1
