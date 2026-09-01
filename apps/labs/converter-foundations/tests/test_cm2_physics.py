"""Physics checks for the Buck/Boost CCM-DCM models."""

import numpy as np
import pytest

from models.cm2_physics import (
    boost_solve,
    buck_solve,
    dcm_boundary,
    i_L_period,
    solve,
)

T = 1e-3  # 1 kHz


def test_boost_transistor_is_ideal_ccm():
    E, R, D, L = 12.0, 5.0, 0.5, 1e-3
    v_out, i_out_avg, i_in_avg, i_pk, i_lo, ccm = boost_solve(E, R, D, L, 'transistor', T)
    assert ccm is True
    assert v_out == pytest.approx(E / (1.0 - D))
    assert E * i_in_avg == pytest.approx(v_out * i_out_avg, rel=1e-6)


def test_solve_dispatches_by_mode():
    args = (12.0, 5.0, 0.5, 1e-3, 'transistor', T)
    assert solve('buck', *args) == buck_solve(*args)
    assert solve('boost', *args) == boost_solve(*args)


def test_boost_light_load_is_dcm_and_boosts_higher():
    E, R, D, L = 12.0, 200.0, 0.5, 20e-6
    v_ccm = E / (1.0 - D)
    v_out, *_rest, ccm = boost_solve(E, R, D, L, 'diode', T)
    assert ccm is False
    assert v_out > v_ccm


@pytest.mark.parametrize('mode', ['buck', 'boost'])
def test_i_L_period_currents_are_non_negative_for_diode(mode):
    phase, i_L, i_in, i_out, *_ = i_L_period(mode, 12.0, 50.0, 0.5, 50e-6, 'diode', T)
    assert np.all(i_L >= -1e-9)
    assert np.all(i_in >= -1e-9)
    assert np.all(i_out >= -1e-9)


@pytest.mark.parametrize('mode', ['buck', 'boost'])
def test_dcm_boundary_is_finite_and_shaped(mode):
    V, I_crit = dcm_boundary(mode, 12.0, 1e-3, 1e3, 40.0)
    assert V.shape == I_crit.shape
    assert np.all(np.isfinite(I_crit))
    assert np.all(I_crit >= 0.0)
