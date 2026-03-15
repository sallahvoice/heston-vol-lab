import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Callable
from app.services.gbm import (black_scholes_call, simulate_gbm_paths)


def monte_carlo_expectation(
    samples : np.ndarray,
    func: Callable[[np.ndarray], np.ndarray]
) -> float:
    return np.mean(func(samples))


def discount_payoff(
    payoff: np.ndarray,
    r: float,
    T: float
    ) -> np.ndarray:
    return np.exp(-r * T) * payoff


def monte_carlo_standard_error(values: np.ndarray) -> float:
    return np.std(values) / np.sqrt(len(values))


def monte_carlo_confidence_interval(
    CL: float,
    abs_error: float,
    se: float
    ) -> bool:
    z = norm.ppf(0.5 + CL/2)
    return abs_error < z * se


def monte_carlo_european_call(
    St: np.ndarray,
    K: float,
    r: float,
    T: float
    ) -> float:

    ST = St[-1]
    n_paths = ST.shape[0]

    payoff = np.maximum(ST - K, 0)
    discounted_payoff = discount_payoff(payoff, r, T)

    price = np.mean(discounted_payoff)

    return price


def monte_carlo_european_put(
    St: np.ndarray,
    K: float,
    r: float,
    T: float
    ) -> float:
   
    ST = St[-1]
    n_paths = ST.shape[0]

    payoff = np.maximum(K - ST, 0)
    discounted_payoff = discount_payoff(payoff, r, T)

    price = np.mean(discounted_payoff)

    return price


def monte_carlo_convergence_test(
    S0: float,
    K: float,
    sigma: float,
    r: float,
    T: float,
    n_steps: int
) -> pd.DataFrame:
    
    bs_price = black_scholes_call(S0, K, sigma, r, T)

    path_counts = [100, 1000, 10000, 100000]
    results = []

    for N in path_counts:
        paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_paths=N)

        mc_price = monte_carlo_european_call(paths, K, r, T)

        ST = paths[-1]
        discounted_payoffs = discount_payoff(np.maximum(ST - K, 0), r, T)
        se = monte_carlo_standard_error(discounted_payoffs, N)

        abs_error = abs(mc_price - bs_price)

        within_95_ci = monte_carlo_confidence_interval(0.95, abs_error, se)
        within_99_ci = monte_carlo_confidence_interval(0.99, abs_error, se)

        results.append({
            "n_paths": N,
            "bs_price": bs_price,
            "mc_price": mc_price,
            "standard_error": se,
            "abs_error": abs_error,
            "theoretical_error": 1 / np.sqrt(N),
            "within_95_ci": within_95_ci,
            "within_99_ci": within_99_ci
        })

    return pd.DataFrame(results)

