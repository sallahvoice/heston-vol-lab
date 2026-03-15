import numpy as np
from scipy.stats import norm
import pandas as pd
from app.services.brownian import simulate_brownian_motion
from app.services.monte_carlo import (monte_carlo_european_call_with_error, )
from app.utils.math_utils import TimeGrid

def simulate_gbm_paths(
    S0: float,
    mu: float,
    sigma:  float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None
) -> np.ndarray:

    grid = TimeGrid.generate_time_grid(n_steps=n_steps, T=T)
    t = grid.time_grid[:, None]

    W, _ = simulate_brownian_motion(n_steps, n_paths, T, seed)

    St = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)

    return St


def simulate_gbm_antihetic(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None
) -> np.ndarray:

    half_n = n_paths // 2

    grid = TimeGrid.generate_time_grid(n_steps=n_steps, T=T)
    t = grid.time_grid[:, None]

    W, _ = simulate_brownian_motion(n_steps, half_n, T, seed)

    W_antihetic = -W
    W_combined = np.concatenate([W, W_antihetic], axis=1)

    St = S0 * np.exp((mu - 0.5 * sigma **2) * T + sigma * W_combined)

    return St


def simulate_gbm_euler(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None
) -> np.ndarray:

    grid = TimeGrid.generate_time_grid(n_steps=n_steps, T=T)
    dt = grid.dt

    St = np.zeros((n_steps, n_paths))
    St[0] = S0

    for t in range(1, n_steps):
        Z = np.random.normal(0, 1, n_paths)
        St[t] = St[t-1] + mu * St[t-1] * dt + sigma * St[t-1] * np.sqrt(dt) * Z
    
    return St


def black_scholes_call(
    S0: float,
    K: float,
    sigma: float,
    r: float,
    T: float
) -> float:

    if T <= 0 or sigma <=0:
        raise ValueError("time to expiry and volatility must be positive")

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)

    call_price = S0 * Nd1 - K * np.exp(-r * T) * Nd2

    return call_price


def gbm_mc_delta(
    S0: float,
    mu: float,
    K: float,
    sigma: float,
    r: float,
    T: float,
    n_steps: int,
    n_paths: int,
    eps: float = 0.01
) -> float:

    paths_up = simulate_gbm_paths(S0 + eps, mu, sigma, T, n_steps, n_paths)
    price_up = monte_carlo_european_call_with_error(paths_up, K, r, T)[0]

    paths_down = simulate_gbm_paths(S0 - eps, mu, sigma, T, n_steps, n_paths)
    price_down = monte_carlo_european_call_with_error(paths_down, K, r, T)[0]

    delta = (price_up - price_down) / (2 * eps)

    return delta


def gbm_moment_match_test(
    St: np.ndarray,
    S0: float,
    mu: float,
    sigma: float,
    T: float
    ) -> dict:

    ST = St[-1]
    simulation_mean = np.mean(ST)
    simulation_var = np.var(ST)

    theoretical_mean = S0 * np.exp(mu * T)
    theoretical_var = (S0**2) * np.exp(2 * mu * T) * (np.exp(sigma**2 * T) - 1)

    mean_error_pct = abs(simulation_mean - theoretical_mean) / theoretical_mean
    var_error_pct = abs(simulation_var - theoretical_var) / theoretical_var

    return {
        "mean_error_pct": mean_error_pct,
        "var_error_pct": var_error_pct
    }