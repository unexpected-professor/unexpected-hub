"""Pure physics/model functions for the fundamentals view — no plotting imports.

Analytic steady-state solvers: Buck CCM/DCM operating point, one-period inductor
current, capacitor ODE steady state, and the iso-power reference grid.
"""

import numpy as np

INIT = dict(E=10.0, R=1.0, Rth=1.0, D=0.6, L=100e-6, C=1e-3)  # L in H, C in F

VI_I_MAX = 26.0
VI_V_MAX = 26.0
CHRONO_Y = 27.0

ISO_POWERS_W = [1, 2, 5, 10, 20, 50, 100, 200]

F_SW = 1e3          # switching frequency (Hz) — 1 kHz, fixed for this demo
T_S = 1.0 / F_SW    # switching period in seconds = 1 ms


def iso_power_grid(i_max=VI_I_MAX, v_max=VI_V_MAX, powers=ISO_POWERS_W):
    """Iso-power hyperbolas (V = P/I) for the V-I plane, plus label anchor points.

    Returns a list of dicts: {'P', 'i' (array), 'v' (array), 'lw', 'label_pos' or None}.
    """
    i_r = np.linspace(0.05, i_max, 1000)
    grid = []
    for P in powers:
        v = P / i_r
        mask = v <= v_max
        lw = 1.3 if P in (10, 20, 50) else 0.8
        i_l, v_l = np.sqrt(P), np.sqrt(P)
        label_pos = (i_l, v_l) if (i_l < i_max * 0.92 and v_l < v_max * 0.92) else None
        grid.append({'P': P, 'i': i_r[mask], 'v': v[mask], 'lw': lw, 'label_pos': label_pos})
    return grid


def buck_solve(E, R, D, L, t2, T=T_S):
    """
    Buck steady-state for both T2 types.
    Returns: v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm
      i_pk — peak current (CCM: avg + ripple/2; DCM: peak from 0)
      i_lo — minimum current (CCM: avg - ripple/2; DCM: 0)
    T — switching period in seconds (default = T_S = 1 ms)
    L — inductance in henries
    """
    delta_ccm = E * D * (1.0 - D) * T / L   # CCM peak-to-peak ripple (A)
    i_avg_ccm = D * E / R

    # Transistor: always CCM, current may go negative
    # Diode: CCM only if i_lo = i_avg - delta/2 >= 0
    ccm = (t2 == 'transistor') or (i_avg_ccm >= delta_ccm / 2.0)

    if ccm:
        v_out = D * E
        i_out_avg = i_avg_ccm
        i_in_avg = D * i_avg_ccm          # D x <i_L>
        i_pk = i_avg_ccm + delta_ccm / 2.0
        i_lo = i_avg_ccm - delta_ccm / 2.0
    else:
        # DCM: solve K*V^2 + E*D^2*V - E^2*D^2 = 0, K = 2L/(R*T)
        K = 2.0 * L / (R * T)
        v_out = E * D * (-D + np.sqrt(D**2 + 4.0 * K)) / (2.0 * K)
        i_pk = (E - v_out) * D * T / L   # peak starting from zero
        i_out_avg = v_out / R
        i_in_avg = D * i_pk / 2.0            # <i_IN> = D*T*i_pk / (2*T)
        i_lo = 0.0

    return v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm


def buck_i_L_period(E, R, D, L_val, t2, N=2000):
    """One period of i_L waveform, consistent with buck_solve."""
    dt = T_S / N
    phase_s = np.linspace(0, T_S, N, endpoint=False)
    v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = buck_solve(E, R, D, L_val, t2)
    slope_up = (E - v_out) / L_val
    slope_dn = v_out / L_val
    if t2 == 'transistor':
        i_L = np.where(phase_s < D * T_S,
                        i_lo + slope_up * phase_s,
                        i_pk - slope_dn * (phase_s - D * T_S))
    elif ccm:
        i_L = np.where(phase_s < D * T_S,
                        i_lo + slope_up * phase_s,
                        i_pk - slope_dn * (phase_s - D * T_S))
        i_L = np.clip(i_L, 0.0, None)
    else:
        t_fall_s = i_pk / slope_dn if slope_dn > 1e-9 else D * T_S
        i_L = np.where(phase_s < D * T_S,
                        slope_up * phase_s,
                        np.where(phase_s < D * T_S + t_fall_s,
                                 i_pk - slope_dn * (phase_s - D * T_S),
                                 0.0))
        i_L = np.clip(i_L, 0.0, None)
    return i_L, dt, v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm


def cap_vout_ss(i_L_period, R, C, dt):
    """
    Steady-state v_out for C*dV/dt + V/R = i_L, zero-order-hold exact solution.
    Stable for all R, C > 0. For large C -> standard ripple formula.
    For small C -> v_out follows i_L*R (case-4 behaviour).
    """
    N = len(i_L_period)
    alpha = np.exp(-dt / (R * C))
    beta = (1.0 - alpha) * R
    # Steady-state IC: find V[0] s.t. V[N] = V[0]
    weights = alpha ** np.arange(N - 1, -1, -1)
    v0_ss = beta * np.dot(weights, i_L_period) / (1.0 - alpha ** N)
    # Reconstruct one period
    v = np.empty(N)
    v[0] = v0_ss
    for k in range(N - 1):
        v[k + 1] = alpha * v[k] + beta * i_L_period[k]
    return v
