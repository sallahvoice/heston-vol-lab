import numpy as np

from app.services.fft_pricing import HestonParams, build_fft_grid, carr_madan_fft_price


def test_build_fft_grid_step_and_shape():
    grid = build_fft_grid(N=32, B=8.0)
    assert grid.shape == (32,)
    assert np.isclose(grid[1] - grid[0], 0.25)


def test_carr_madan_fft_price_output_and_finite_values():
    params = HestonParams(v0=0.04, r=0.01, kappa=1.5, theta=0.04, rho=0.5, xi=0.3)

    k, c = carr_madan_fft_price(params, T=1.0, S0=100.0, alpha=1.5, N=512, B=100.0)

    assert k.shape == (512,)
    assert c.shape == (512,)
    assert np.all(np.isfinite(k))
    assert np.all(np.isfinite(c))