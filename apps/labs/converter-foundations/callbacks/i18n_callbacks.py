from dash.dependencies import Input, Output, State

from i18n import t

_MODE_KEYS = [
    ('direct', 'mode_direct'),
    ('rth', 'mode_rth'),
    ('switch', 'mode_switch'),
    ('buck', 'mode_buck'),
    ('cap', 'mode_cap'),
]

_MODE_KEYS_CM2 = [
    ('buck', 'mode_buck2'),
    ('boost', 'mode_boost2'),
]

# (tooltip component id, i18n key) — several ids intentionally share the same key since the
# underlying control (and its hint) is identical between CM1 and CM2.
_TOOLTIPS = [
    ('tt-mode-select', 'tt_mode_select'),
    ('tt-panel-visibility', 'tt_panel_visibility'),
    ('tt-show-iminmax', 'tt_show_iminmax'),
    ('tt-slider-E', 'tt_slider_E'),
    ('tt-slider-R', 'tt_slider_R'),
    ('tt-slider-Rth', 'tt_slider_Rth'),
    ('tt-slider-D', 'tt_slider_D'),
    ('tt-slider-L', 'tt_slider_L'),
    ('tt-slider-C', 'tt_slider_C'),
    ('tt-toggle-left-btn', 'tt_pane_toggle'),
    ('tt-toggle-right-btn', 'tt_pane_toggle'),
    ('tt-cm2-mode-select', 'tt_mode_select2'),
    ('tt-cm2-panel-visibility', 'tt_panel_visibility'),
    ('tt-cm2-show-dcmzone', 'tt_show_dcmzone'),
    ('tt-cm2-show-iminmax', 'tt_show_iminmax'),
    ('tt-cm2-slider-E', 'tt_slider_E'),
    ('tt-cm2-slider-R', 'tt_slider_R'),
    ('tt-cm2-slider-D', 'tt_slider_D'),
    ('tt-cm2-slider-L', 'tt_slider_L'),
    ('tt-cm2-slider-F', 'tt_slider_F'),
    ('tt-cm2-slider-C', 'tt_slider_C'),
    ('tt-cm2-toggle-left-btn', 'tt_pane_toggle'),
    ('tt-cm2-toggle-right-btn', 'tt_pane_toggle'),
    ('tt-t2-select', 'tt_switch_select'),
    ('tt-cm2-t2-select', 'tt_switch_select'),
    ('tt-lang-toggle', 'tt_lang_toggle'),
]


def register_i18n_callbacks(app):
    @app.callback(
        Output('lang-store', 'data'),
        Input('lang-toggle-btn', 'n_clicks'),
        State('lang-store', 'data'),
        prevent_initial_call=True,
    )
    def toggle_lang(_n_clicks, lang):
        return 'en' if lang == 'fr' else 'fr'

    @app.callback(
        Output('lang-toggle-btn', 'children'),
        Output('app-title', 'children'),
        Output('circuit-view-title', 'children'),
        Output('cas-title', 'children'),
        Output('affichage-title', 'children'),
        Output('parameters-title', 'children'),
        Output('mode-select', 'options'),
        Output('panel-visibility', 'options'),
        Input('lang-store', 'data'),
    )
    def apply_language(lang):
        lang = lang or 'fr'
        next_lang_label = 'FR' if lang == 'en' else 'EN'
        mode_options = [{'label': t(key, lang), 'value': value} for value, key in _MODE_KEYS]
        panel_options = [
            {'label': t('plan_vi', lang), 'value': 'vi'},
            {'label': t('chrono_label', lang), 'value': 'chrono'},
        ]
        return (
            next_lang_label,
            t('title', lang),
            t('circuit_view', lang),
            t('cas', lang),
            t('affichage', lang),
            t('parameters', lang),
            mode_options,
            panel_options,
        )

    @app.callback(
        Output('cm2-app-title', 'children'),
        Output('cm2-circuit-view-title', 'children'),
        Output('cm2-cas-title', 'children'),
        Output('cm2-affichage-title', 'children'),
        Output('cm2-parameters-title', 'children'),
        Output('cm2-switch-title', 'children'),
        Output('cm2-mode-select', 'options'),
        Output('cm2-panel-visibility', 'options'),
        Output('cm2-show-dcmzone', 'options'),
        Input('lang-store', 'data'),
    )
    def apply_language_cm2(lang):
        lang = lang or 'fr'
        mode_options = [{'label': t(key, lang), 'value': value} for value, key in _MODE_KEYS_CM2]
        panel_options = [
            {'label': t('plan_vi', lang), 'value': 'vi'},
            {'label': t('chrono_label', lang), 'value': 'chrono'},
            {'label': t('voutd_label', lang), 'value': 'voutd'},
        ]
        dcmzone_options = [{'label': t('dcm_zone_label', lang), 'value': 'on'}]
        return (
            t('title2', lang),
            t('circuit_view', lang),
            t('cas', lang),
            t('affichage', lang),
            t('parameters', lang),
            t('switch_label', lang),
            mode_options,
            panel_options,
            dcmzone_options,
        )

    @app.callback(
        [Output(tooltip_id, 'children') for tooltip_id, _ in _TOOLTIPS],
        Input('lang-store', 'data'),
    )
    def apply_tooltips(lang):
        lang = lang or 'fr'
        return [t(key, lang) for _, key in _TOOLTIPS]
