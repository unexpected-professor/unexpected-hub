"""Minimal FR/EN string catalog for the laboratory UI and figures."""

TEXT = {
    'title': {
        'fr': 'Fondamentaux de la conversion de puissance',
        'en': 'Power Conversion Fundamentals',
    },
    'circuit_view': {'fr': 'Vue du circuit', 'en': 'Circuit view'},
    'cas': {'fr': 'Cas', 'en': 'Case'},
    'parameters': {'fr': 'Paramètres', 'en': 'Parameters'},
    'affichage': {'fr': 'Affichage', 'en': 'Display'},
    'plan_vi': {'fr': 'Plan V-I', 'en': 'V-I plane'},
    'chrono_label': {'fr': 'Chrono.', 'en': 'Waveforms'},

    'mode_direct': {'fr': '1 – Direct (E, R)', 'en': '1 – Direct (E, R)'},
    'mode_rth': {'fr': '2 – Série (+ Rth)', 'en': '2 – Series (+ Rth)'},
    'mode_switch': {'fr': '3 – Interrupteur (+ D)', 'en': '3 – Switch (+ D)'},
    'mode_buck': {'fr': '4 – Buck (+ D, L)', 'en': '4 – Buck (+ D, L)'},
    'mode_cap': {'fr': '5 – Buck + C (+ C)', 'en': '5 – Buck + C (+ C)'},

    'vi_title': {'fr': 'Plan tension-courant', 'en': 'Voltage-current plane'},
    'chrono_title': {'fr': 'Chronogramme', 'en': 'Waveforms'},
    'axis_current': {'fr': 'Courant (A)', 'en': 'Current (A)'},
    'axis_voltage': {'fr': 'Tension (V)', 'en': 'Voltage (V)'},
    'axis_time': {'fr': 'Temps (ms)', 'en': 'Time (ms)'},
    'axis_chrono_y': {'fr': 'Tension (V) ou Courant (A)', 'en': 'Voltage (V) or Current (A)'},

    'charge_r': {'fr': 'Charge R = {R:.2f} Ω', 'en': 'Load R = {R:.2f} Ω'},
    'k_closed': {'fr': '(K fermé)', 'en': '(K closed)'},
    'k_open': {'fr': '(K ouvert)', 'en': '(K open)'},
    'vout_pulsed_fem': {'fr': 'V_OUT pulsée   RMS={v_rms:.2f} V', 'en': 'V_OUT pulsed   RMS={v_rms:.2f} V'},
    'iout_pulsed': {'fr': 'I_OUT pulsé    RMS={i_rms:.2f} A', 'en': 'I_OUT pulsed    RMS={i_rms:.2f} A'},
    'iin_pulsed_rms': {'fr': 'I_IN  pulsé    RMS={i_rms:.2f} A', 'en': 'I_IN  pulsed    RMS={i_rms:.2f} A'},
    'iin_pulsed_t1': {'fr': 'I_IN  pulsé T1   ⟨⟩={i_in_avg:.2f} A', 'en': 'I_IN  pulsed T1   ⟨⟩={i_in_avg:.2f} A'},
    'iin_pulsed_t1_lower': {
        'fr': 'i_IN pulsé T1   ⟨⟩={i_in_avg:.2f} A', 'en': 'i_IN pulsed T1   ⟨⟩={i_in_avg:.2f} A',
    },
    'out_of_plane': {'fr': '  (i_L < 0 hors plan)', 'en': '  (i_L < 0 out of range)'},
    'dcm_banner': {'fr': 'DCM — T2 diode bloque', 'en': 'DCM — T2 diode blocked'},

    # CM2-specific
    'title2': {
        'fr': 'Conduction continue et discontinue (Buck – Boost)',
        'en': 'Continuous and Discontinuous Conduction (Buck – Boost)',
    },
    'mode_buck2': {'fr': 'Buck (dévolteur)', 'en': 'Buck (step-down)'},
    'mode_boost2': {'fr': 'Boost (survolteur)', 'en': 'Boost (step-up)'},
    'voutd_label': {'fr': 'Vout(D)', 'en': 'Vout(D)'},
    'dcm_zone_label': {'fr': 'Zone DCM', 'en': 'DCM zone'},
    'switch_label': {'fr': 'Interrupteur', 'en': 'Switch'},
    'axis_time_norm': {'fr': 'Temps normalisé  t / T', 'en': 'Normalized time  t / T'},
    'vout_avg': {'fr': 'V_OUT   ⟨⟩={v_out:.2f} V', 'en': 'V_OUT   ⟨⟩={v_out:.2f} V'},
    'il_avg': {'fr': 'i_L   ⟨⟩={i_avg:.2f} A', 'en': 'i_L   ⟨⟩={i_avg:.2f} A'},
    'iout_avg': {'fr': 'I_OUT   ⟨⟩={i_out_avg:.2f} A', 'en': 'I_OUT   ⟨⟩={i_out_avg:.2f} A'},
    'iin_avg': {'fr': 'I_IN   ⟨⟩={i_in_avg:.2f} A', 'en': 'I_IN   ⟨⟩={i_in_avg:.2f} A'},
    'dcm_banner2': {
        'fr': "DCM — le courant i_L s'annule", 'en': 'DCM — the inductor current i_L reaches zero',
    },
    'axis_duty': {'fr': 'Rapport cyclique D', 'en': 'Duty cycle D'},
    'voutd_title': {
        'fr': 'V_OUT = f(D) — courbe réelle vs. idéale (CCM)',
        'en': 'V_OUT = f(D) — real vs. ideal curve (CCM)',
    },
    'voutd_ideal': {'fr': 'Idéal (CCM), R,L,f→∞', 'en': 'Ideal (CCM), R,L,f→∞'},
    'voutd_ccm': {'fr': 'Conduction continue (CCM)', 'en': 'Continuous conduction (CCM)'},
    'voutd_dcm': {'fr': 'Conduction discontinue (DCM)', 'en': 'Discontinuous conduction (DCM)'},
    'voutd_operating': {
        'fr': 'Point de fonctionnement : V_OUT={v_now:.2f} V ({regime})',
        'en': 'Operating point: V_OUT={v_now:.2f} V ({regime})',
    },

    # Tooltips (shared between CM1 and CM2 where the control is identical)
    'tt_mode_select': {'fr': 'Choisissez le montage à étudier', 'en': 'Choose the circuit configuration to study'},
    'tt_mode_select2': {'fr': 'Choisissez la topologie à étudier', 'en': 'Choose the topology to study'},
    'tt_panel_visibility': {
        'fr': 'Afficher/masquer les graphiques ci-contre', 'en': 'Show/hide the graphs alongside',
    },
    'tt_show_iminmax': {
        'fr': 'Afficher les repères de courant/puissance min et max',
        'en': 'Show the min/max current and power markers',
    },
    'tt_show_dcmzone': {
        'fr': 'Mettre en évidence la zone de conduction discontinue (visible uniquement en mode Diode)',
        'en': 'Highlight the discontinuous-conduction zone (only visible in Diode mode)',
    },
    'tt_slider_E': {'fr': 'Modifier la tension de la source', 'en': 'Change the source voltage'},
    'tt_slider_R': {'fr': 'Modifier la résistance de charge', 'en': 'Change the load resistance'},
    'tt_slider_Rth': {
        'fr': 'Modifier la résistance de Thévenin de la source',
        'en': "Change the source's Thevenin resistance",
    },
    'tt_slider_D': {'fr': 'Modifier le rapport cyclique', 'en': 'Change the duty cycle'},
    'tt_slider_L': {'fr': "Modifier l'inductance", 'en': 'Change the inductance'},
    'tt_slider_F': {'fr': 'Modifier la fréquence de découpage', 'en': 'Change the switching frequency'},
    'tt_slider_C': {'fr': 'Modifier la capacité de sortie', 'en': 'Change the output capacitance'},
    'tt_pane_toggle': {'fr': 'Afficher/masquer ce panneau', 'en': 'Show/hide this panel'},
    'tt_switch_select': {
        'fr': 'Basculer entre MOSFET (toujours en conduction continue) et Diode (peut entrer en conduction discontinue)',
        'en': 'Toggle between MOSFET (always continuous conduction) and Diode (can enter discontinuous conduction)',
    },
    'tt_lang_toggle': {'fr': 'Change language', 'en': 'Change language'},
}


def t(key, lang='fr', **fmt):
    template = TEXT[key].get(lang, TEXT[key]['fr'])
    return template.format(**fmt) if fmt else template
