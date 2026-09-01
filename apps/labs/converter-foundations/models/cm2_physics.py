"""Pure physics/model functions for the Buck/Boost CCM-DCM view.

`cap_vout_ss` and `iso_power_grid` are topology-agnostic and already live in
`converter_physics.py` — reused here rather than duplicated.
"""

import numpy as np

INIT = dict(E=12.0, R=2.0, D=0.5, L=1e-3, F=1e3, C=1e-4)  # L in H, F in Hz, C in F

VI_I_MAX = 16.0
VI_V_MAX = 40.0
CHRONO_Y = 42.0


def buck_solve(E, R, D, L, sw, T):
    """Buck steady-state. Returns v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm."""
    delta_ccm = E * D * (1.0 - D) * T / L
    i_avg_ccm = D * E / R
    ccm = (sw == 'transistor') or (i_avg_ccm >= delta_ccm / 2.0)
    if ccm:
        v_out = D * E
        i_out_avg = i_avg_ccm
        i_in_avg = D * i_avg_ccm
        i_pk = i_avg_ccm + delta_ccm / 2.0
        i_lo = i_avg_ccm - delta_ccm / 2.0
    else:
        K = 2.0 * L / (R * T)
        v_out = E * D * (-D + np.sqrt(D**2 + 4.0 * K)) / (2.0 * K)
        i_pk = (E - v_out) * D * T / L
        i_out_avg = v_out / R
        i_in_avg = D * i_pk / 2.0
        i_lo = 0.0
    return v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm


def boost_solve(E, R, D, L, sw, T):
    """Boost steady-state. Returns v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm."""
    delta_ccm = E * D * T / L
    i_L_avg_ccm = E / (R * (1.0 - D) ** 2)
    i_lo_ccm = i_L_avg_ccm - delta_ccm / 2.0
    ccm = (sw == 'transistor') or (i_lo_ccm >= 0.0)
    if ccm:
        v_out = E / (1.0 - D)
        i_out_avg = v_out / R
        i_in_avg = i_L_avg_ccm
        i_pk = i_L_avg_ccm + delta_ccm / 2.0
        i_lo = i_lo_ccm
    else:
        v_out = E * (1.0 + np.sqrt(1.0 + 2.0 * D**2 * R * T / L)) / 2.0
        i_pk = E * D * T / L
        i_lo = 0.0
        i_out_avg = v_out / R
        delta2 = E * D / (v_out - E)
        i_in_avg = i_pk * (D + delta2) / 2.0
    return v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm


def solve(mode, E, R, D, L, sw, T):
    return buck_solve(E, R, D, L, sw, T) if mode == 'buck' else boost_solve(E, R, D, L, sw, T)


def buck_i_L_period(E, R, D, L, sw, T, N=2000):
    """One period of i_L(phase) for the buck, phase in [0, T)."""
    phase = np.linspace(0, T, N, endpoint=False)
    v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = buck_solve(E, R, D, L, sw, T)
    slope_up = (E - v_out) / L
    slope_dn = v_out / L
    if sw == 'transistor':
        i_L = np.where(phase < D * T,
                        i_lo + slope_up * phase,
                        i_pk - slope_dn * (phase - D * T))
    elif ccm:
        i_L = np.where(phase < D * T,
                        i_lo + slope_up * phase,
                        i_pk - slope_dn * (phase - D * T))
        i_L = np.clip(i_L, 0.0, None)
    else:
        t_fall = i_pk / slope_dn if slope_dn > 1e-9 else D * T
        i_L = np.where(phase < D * T,
                        slope_up * phase,
                        np.where(phase < D * T + t_fall,
                                 i_pk - slope_dn * (phase - D * T),
                                 0.0))
        i_L = np.clip(i_L, 0.0, None)
    i_in = np.where(phase < D * T, i_L, 0.0)   # T1 conducts during ON only
    i_out = i_L                                 # buck: L feeds R at all times
    return phase, i_L, i_in, i_out, v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm


def boost_i_L_period(E, R, D, L, sw, T, N=2000):
    """One period of i_L(phase) for the boost, phase in [0, T)."""
    phase = np.linspace(0, T, N, endpoint=False)
    v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = boost_solve(E, R, D, L, sw, T)
    slope_up = E / L
    slope_dn = (v_out - E) / L
    if sw == 'transistor':
        i_L = np.where(phase < D * T,
                        i_lo + slope_up * phase,
                        i_pk - slope_dn * (phase - D * T))
    elif ccm:
        i_L = np.where(phase < D * T,
                        i_lo + slope_up * phase,
                        i_pk - slope_dn * (phase - D * T))
        i_L = np.clip(i_L, 0.0, None)
    else:
        t_fall = i_pk / slope_dn if slope_dn > 1e-9 else (1.0 - D) * T
        i_L = np.where(phase < D * T,
                        slope_up * phase,
                        np.where(phase < D * T + t_fall,
                                 i_pk - slope_dn * (phase - D * T),
                                 0.0))
        i_L = np.clip(i_L, 0.0, None)
    i_in = i_L                                   # boost: L is always in the input branch
    i_out = np.where(phase < D * T, 0.0, i_L)    # output only fed while T1 is OFF
    return phase, i_L, i_in, i_out, v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm


def i_L_period(mode, E, R, D, L, sw, T, N=2000):
    fn = buck_i_L_period if mode == 'buck' else boost_i_L_period
    return fn(E, R, D, L, sw, T, N=N)


def dcm_boundary(mode, E, L, f, v_max):
    """CCM/DCM boundary I_crit(V) in the (I, V) plane — independent of D and R.

    Derived by eliminating D between the CCM transfer function (V = f(D)) and
    the critical-current condition I_crit(D) = E*D(1-D)/(2Lf):
      buck  : I_crit(V) = V(E-V) / (2 E L f),         0 <= V <= E
      boost : I_crit(V) = E^2(V-E) / (2 L f V^2),      E <= V <= v_max
    Points with I < I_crit(V) are in DCM.
    """
    if mode == 'buck':
        V = np.linspace(0.0, E, 300)
        I_crit = V * (E - V) / (2.0 * E * L * f)
    else:
        V = np.linspace(E, max(v_max, E * 1.01), 300)
        I_crit = E**2 * (V - E) / (2.0 * L * f * V**2)
    return V, np.clip(I_crit, 0.0, None)
