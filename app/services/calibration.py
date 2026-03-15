import numpy as np
from scipy.optimize import minimize
from app.services.heston import HestonParams
from app.services.fft_pricing import carr_madan_fft_price
from app.services.heston import check_feller_condition


def heston_objective(
    params: HestonParams,
    K: np.ndarray,
    T: np.ndarray,
    S0: float,
    alpha: float,
    N: int,
    B: float,
    market_prices: np.ndarray
) -> float:

    model_prices = np.array((
        carr_madan_fft_price(params, T=t, S0=S0, alpha=alpha, N=N, B=B)[1][0]
        for t in T
    ))

    err = np.sum((market_prices - model_prices)**2) / len(market_prices)
    feller_condition =  check_feller_condition(theta=params.theta, kappa=params.kappa)
    if not feller_condition:
        err += 1e6

    return err


def calibrate_heston_objective(
    initial_guess: HestonParams,
    K: np.ndarray,
    T: np.ndarray,
    S0: float,
    market_prices: np.ndarray,
    alpha: float = 1.5,
    N: int = 2**12,
    B: float = 1000,
    bounds=None,
    method: str = "L-BFGS-B",
    tol: float = 1e-6,
    options: dict = None,
) -> tuple[HestonParams, float]:

    def objective_wrapper(x):
        p = HestonParams(*x)
        return heston_objective(p, K, T, S0, alpha, N, B, market_prices)
    
    x0 = np.array([
        initial_guess.v0,
        initial_guess.r,
        initial_guess.kappa,
        initial_guess.theta,
        initial_guess.rho,
        initial_guess.xi
        ])

    result = minimize(
        objective_wrapper,
        x0,
        method=method, options=options,
        bounds=bounds,
        tol = tol,
        options=options
        )

    calibrated_params = HestonParams(*result.x)
    return calibrated_params, result.fun


def calibration_error_summary(
    calibrated_params: HestonParams,
    K: np.ndarray,
    T: np.ndarray,
    S0,
    market_prices: np.ndarray,
    alpha: float = 1.5,
    N: int = 2**12,
    B: float = 1000
) -> dict:

    model_prices = np.array([
        carr_madan_fft_price(calibrated_params, T=t, S0=S0, alpha=alpha, N=N, B=B)[1][0]
        for t in T
    ])

    abs_errors = np.abs(model_prices - market_prices)
    rmse = np.sqrt(np.mean(abs_errors**2))

    return {
        "market_prices": market_prices,
        "model_prices": model_prices,
        "abs_errors": abs_errors,
        "rmse": rmse
    }