"""Physics checks for the fundamentals models against known analytic results."""

import numpy as np
import pytest

from models.converter_physics import (
    T_S,
    buck_solve,
    buck_i_L_period,
    cap_vout_ss,
    iso_power_grid,
)


def test_buck_transistor_is_ideal_ccm():
    # A synchronous (transistor) Buck is always in CCM: V_OUT = D * E exactly.
    E, R, D, L = 12.0, 4.0, 0.4, 1e-3
    v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = buck_solve(E, R, D, L, 'transistor')
    assert ccm is True
    assert v_out == pytest.approx(D * E)
    assert i_out_avg == pytest.approx(D * E / R)
    # Input/output power balance for the lossless model.
    assert E * i_in_avg == pytest.approx(v_out * i_out_avg, rel=1e-6)


def test_buck_diode_enters_dcm_at_light_load():
    # Large R (light load) + small L pushes a diode-rectified Buck into DCM,
    # where V_OUT rises above the ideal D * E.
    E, R, D, L = 12.0, 80.0, 0.4, 20e-6
    v_out, *_rest, ccm = buck_solve(E, R, D, L, 'diode')
    assert ccm is False
    assert v_out > D * E


def test_buck_i_L_period_is_consistent_with_solve():
    E, R, D, L = 10.0, 2.0, 0.5, 500e-6
    i_L, dt, v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = buck_i_L_period(
        E, R, D, L, 'transistor'
    )
    assert i_L.shape[0] * dt == pytest.approx(T_S)
    # Mean of the inductor-current waveform equals the reported output average.
    assert i_L.mean() == pytest.approx(i_out_avg, rel=2e-2)


def test_cap_vout_ss_large_capacitor_flattens_ripple():
    E, R, D, L = 10.0, 2.0, 0.5, 200e-6
    i_L, dt, *_ = buck_i_L_period(E, R, D, L, 'transistor')
    small_C = cap_vout_ss(i_L, R, 1e-6, dt)
    large_C = cap_vout_ss(i_L, R, 1e-2, dt)
    assert np.ptp(large_C) < np.ptp(small_C)
    assert large_C.mean() == pytest.approx((i_L * R).mean(), rel=5e-2)


def test_iso_power_grid_masks_to_the_visible_quadrant():
    grid = iso_power_grid(i_max=26.0, v_max=26.0, powers=[1, 10, 100])
    assert [g['P'] for g in grid] == [1, 10, 100]
    for entry in grid:
        assert np.all(entry['v'] <= 26.0 + 1e-9)
        assert entry['i'].shape == entry['v'].shape
