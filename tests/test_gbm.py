import numpy as np
import pytest

from app.services.gbm import (
    black_scholes_call, 
    gbm_moment_match_test, 
    simulate_gbm_paths,
)



def test_simulate_gbm_paths_and_shape_and_initial_value():
    paths = simulate_gbm_paths(
        S0=100.0,
        mu=0.05,
        sigma=0.2,
        T=1.0,
        n_steps=50,
        n_paths=100,
        seed=4,
    )

    assert paths.shape == (50, 100)
    assert np.allclose(paths[0], 100.0)


def test_black_scholes_call_validates_inputs():
    with pytest.raises(ValueError):
        black_scholes_call(S0=100.0, K=100.0, sigma=0.0, r=0.01, T=1.0)

    with pytest.raises(ValueError):
        black_scholes_call(S0=100.0, K=100.0, sigma=0.2, r=0.01, T=0.0)


def test_gmb_moment_match_returns_expected_keys():
    paths = simulate_gbm_paths(
        S0=100.0,
        mu=0.04,
        sigma=0.23,
        T=1.0,
        n_steps=60,
        n_paths=150,
        seed=11,     
    )

    result = gbm_moment_match_test(
        paths,
        S0=100.0,
        mu=0.04,
        sigma=0.23,
        T=1.0,
    )
    
    assert set(result.keys()) == {"mean_error_pct", "var_error_pct"}
    assert result["mean_error_pct"] >= 0
    assert result["var_error_pct"] >= 0