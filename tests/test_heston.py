import numpy as np

from app.services.heston import (
    check_feller_condition,
    heston_price_update,
    heston_variance_full_truncation,
    simulate_heston_paths,
)


def test_simulate_heston_paths_shapes_and_initial_values():
    S, v = simulate_heston_paths(
        S0=100.0,
        v0=0.04,
        rho=0.3,
        T=1.0,
        n_steps=40,
        n_paths=100,
        mu=0.02,
        theta=0.03,
        kappa=1.2,
        xi=0.3,
        seed=19,
    )

    assert S.shape == (40, 100)
    assert v.shape == (40, 100)
    assert np.allclose(S[0], 100.0)
    assert np.allclose(v[0], 0.04)


def test_variance_and_price_updates_are_stable_for_zero_noice():
    dW = np.zeros((9, 4))
    v = heston_variance_full_truncation(
        v0=0.04,
        dW2=dW,
        dt=0.05,
        theta=0.03,
        kappa=1.2,
        xi=0.3,
    )
    S = heston_price_update(
        S0=100.0,
        mu=0.03,
        vt=v,
        dW1=dW,
        dt=0.1,
    )

    assert np.all(v >= 0)
    assert np.all(np.isfinite(S))


def test_feller_condition_boolean():
    assert check_feller_condition(theta=0.04, kappa=3.0, xi=0.3) is True
    assert check_feller_condition(theta=0.02, kappa=0.2, xi=0.6) is False