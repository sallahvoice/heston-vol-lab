import numpy as np

from app.services.calibration import (
    _merge_optimizer_options,
    _model_prices_for_quotes,
    calibrate_heston_objective,
)
from app.services.fft_pricing import HestonParams


def test_model_prices_are_filled_when_surface_cache_hits(monkeypatch):
    params = HestonParams(v0=0.04, r=0.01, kappa=1.0, theta=0.04, rho=-0.5, xi=0.3)
    strikes = np.array([90.0, 100.0, 110.0])
    maturities = np.array([1.0, 1.0, 1.0])

    k_grid = np.log(np.array([80.0, 100.0, 120.0]))
    c_grid = np.array([21.0, 12.0, 6.0])

    params_key = (params.v0, params.r, params.kappa, params.theta, params.rho, params.xi)
    cache_key = (params_key, 1.0, 1.5, 16, 200.0)
    surface_cache = {cache_key: (k_grid, c_grid)}

    call_counter = {"count": 0}

    def fake_fft(*args, **kwargs):
        call_counter["count"] += 1
        return k_grid, c_grid

    monkeypatch.setattr("app.services.calibration.carr_madan_fft_price", fake_fft)

    model = _model_prices_for_quotes(
        params=params,
        K=strikes,
        T=maturities,
        S0=100.0,
        alpha=1.5,
        N=16,
        B=200.0,
        surface_cache=surface_cache,
    )

    assert np.all(np.isfinite(model))
    assert np.allclose(model, np.array([16.5, 12.0, 9.0]))
    assert call_counter["count"] == 0


def test_calibration_uses_objective_cache_for_near_identical_x(monkeypatch):
    initial = HestonParams(v0=0.04, r=0.01, kappa=1.2, theta=0.04, rho=-0.3, xi=0.4)
    K = np.array([100.0])
    T = np.array([1.0])
    market_prices = np.array([12.0])

    call_counter = {"count": 0}

    def fake_objective(*args, **kwargs):
        call_counter["count"] += 1
        return 0.123

    class FakeResult:
        def __init__(self, x):
            self.x = x
            self.fun = 0.123
            self.success = True
            self.message = "ok"
            self.nit = 1

    def fake_minimize(fun, x0, **kwargs):
        x1 = x0.copy()
        x2 = x0.copy()
        x2[0] += 1e-11
        fun(x1)
        fun(x2)
        return FakeResult(x0)

    monkeypatch.setattr("app.services.calibration.heston_objective", fake_objective)
    monkeypatch.setattr("app.services.calibration.minimize", fake_minimize)

    calibrate_heston_objective(
        initial_guess=initial,
        K=K,
        T=T,
        S0=100.0,
        market_prices=market_prices,
        options={"maxiter": 5},
    )

    assert call_counter["count"] == 1


def test_merge_optimizer_options_allows_overrides():
    merged = _merge_optimizer_options({"maxiter": 10, "disp": True})
    assert merged["maxiter"] == 10
    assert merged["maxfun"] == 5000
    assert merged["disp"] is True