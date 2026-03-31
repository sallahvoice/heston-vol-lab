import numpy as np
from scipy.optimize import minimize

from app.services.fft_pricing import HestonParams, carr_madan_fft_price
from app.services.calibration_constraints import evaluate_heston_constraints
from app.utils.decorators import log_optimizer, timing

FELLER_PENALTY = 1e6
DEFAULT_OPTIMIZER_OPTIONS = {
    "maxiter": 300,
    "maxfun": 5000,
    "ftol": 1e-12,
}
OBJECTIVE_CACHE_DECIMAL = 10

def _validate_and_broadcast_inputs(
    K: np.ndarray | list[float] | float,
    T: np.ndarray | list[float] | float,
    market_prices: np.ndarray | list[float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    strikes = np.atleast_1d(np.asarray(K, dtype=float))
    maturities = np.atleast_1d(np.asarray(T, dtype=float))
    market = np.atleast_1d(np.asarray(market_prices, dtype=float))

    if np.any(strikes <= 0):
        raise ValueError("All strikes K must be positive.")
    if np.any(maturities <= 0):
        raise ValueError("All maturities T must be positive.")
    
    n = market.shape[0]

    if strikes.size == 1 and n > 1:
        strikes = np.full(n, strikes.item())
    if maturities.size == 1 and n > 1:
        maturities = np.full(n, maturities.item())

    if not (strikes.size == maturities.size == n):
        raise ValueError(
            "K, T, and market_prices must have compatible lengths"
            "(or K/T can be scalars)."
        )
    
    return strikes, maturities, market


def _model_prices_for_quotes(
    params: HestonParams,
    K: np.ndarray,
    T: np.ndarray,
    S0: float,
    alpha: float,
    N: int,
    B: float,
    surface_cache: dict[tuple[tuple[float, ...], float, float, int, float], tuple[np.ndarray, np.ndarray]] | None = None,
) -> np.ndarray:

    model_prices = np.empty_like(K, dtype=float)
    params_key = _params_cache_key(params)

    unique_T = np.unique(T)
    for t in unique_T:
        idx = T == t
        cache_key = (params_key, float(t), alpha, N, B)
        if surface_cache is not None and cache_key in surface_cache:
            k_grid, c_grid = surface_cache[cache_key]
        else:
            k_grid, c_grid = carr_madan_fft_price(
                params=params,
                T=float(t),
                S0=S0,
                alpha=alpha,
                N=N,
                B=B
            )
            if surface_cache is not None:
                surface_cache[cache_key] = (k_grid, c_grid)
        strike_grid = np.exp(k_grid)
        model_prices[idx] = np.interp(K[idx], strike_grid, c_grid)
    
    return model_prices


def heston_objective(
    params: HestonParams,
    K: np.ndarray,
    T: np.ndarray,
    S0: float,
    alpha: float,
    N: int,
    B: float,
    market_prices: np.ndarray,
    surface_cache: dict[tuple[tuple[float, ...], float, float, int, float], tuple[np.ndarray, np.ndarray]] | None = None,
) -> float:

    model_prices = _model_prices_for_quotes(
        params,
        K,
        T,
        S0,
        alpha,
        N,
        B,
        surface_cache=surface_cache,
    )

    err = float(np.mean((market_prices - model_prices) ** 2))

    constraints = evaluate_heston_constraints(
        v0=params.v0,
        kappa=params.kappa,
        theta=params.theta,
        rho=params.rho,
        xi=params.xi
    )
    err += constraints.penalty

    return err


def _params_cache_key(
    params: HestonParams,
    decimals: int = OBJECTIVE_CACHE_DECIMAL,
) -> tuple[float, ...]:
    raw = np.asarray(
        [params.v0, params.r, params.kappa, params.theta, params.rho, params.xi],
        dtype=float
    )

    return tuple(np.round(raw, decimals))


def _merge_optimizer_options(options: dict | None) -> dict:
    merged = DEFAULT_OPTIMIZER_OPTIONS.copy()
    if options:
        merged.update(options)

    return merged


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
    options: dict | None = None,
    surface_cache: dict[tuple[tuple[float, ...], float, float, int, float], tuple[np.ndarray, np.ndarray]] | None = None,
) -> tuple[HestonParams, float, bool, str]:

    k_arr, T_arr, market_arr = _validate_and_broadcast_inputs(K, T, market_prices)
    objective_cache: dict[tuple[float, ...], float] = {}
    resolved_options = _merge_optimizer_options(options)

    def objective_wrapper(x: np.ndarray) -> float:
        cache_key = tuple(np.round(x, OBJECTIVE_CACHE_DECIMAL))
        if cache_key in objective_cache:
            return objective_cache[cache_key]
        p = HestonParams(*x)
        value = heston_objective(
            p,
            k_arr,
            T_arr,
            S0,
            alpha,
            N,
            B,
            market_arr,
            surface_cache=surface_cache,
        )
        objective_cache[cache_key] = value
        return value
    
    x0 = np.array(
        [
            initial_guess.v0,
            initial_guess.r,
            initial_guess.kappa,
            initial_guess.theta,
            initial_guess.rho,
            initial_guess.xi,
        ],
        dtype=float,
    )

    @log_optimizer
    def _run_optimization():
        return minimize(
            objective_wrapper,
            x0,
            method=method,
            bounds=bounds,
            tol=tol,
            options=resolved_options,
            )

    result = _run_optimization()

    calibrated_params = HestonParams(*result.x)

    return (
        calibrated_params,
        float(result.fun),
        bool(result.success),
        str(result.message),
    )


def calibration_error_summary(
    calibrated_params: HestonParams,
    K: np.ndarray,
    T: np.ndarray,
    S0: float,
    market_prices: np.ndarray,
    alpha: float = 1.5,
    N: int = 2**12,
    B: float = 1000,
) -> dict:

    K_arr, T_arr, market_arr = _validate_and_broadcast_inputs(K, T, market_prices)

    model_prices = _model_prices_for_quotes(
        calibrated_params,
        K_arr,
        T_arr,
        S0,
        alpha,
        N,
        B,
    )

    abs_errors = np.abs(model_prices - market_arr)
    rmse = float(np.sqrt(np.mean(abs_errors**2)))

    return {
        "market_prices": market_arr,
        "model_prices": model_prices,
        "abs_errors": abs_errors,
        "rmse": rmse,
    }


@timing
def calibrate_heston(
    initial_guess: HestonParams,
    K: np.ndarray,
    T: np.ndarray,
    S0: float,
    market_prices: np.ndarray,
    alpha: float = 1.5,
    N: int = 2**12,
    B: float = 1000,
    method: str = "L-BFGS-B",
    tol: float = 1e-6,
    bounds=None,
    options: dict | None = None,
) -> dict:

    params, _loss, _success, _message = calibrate_heston_objective(
        initial_guess=initial_guess,
        K=K,
        T=T,
        S0=S0,
        market_prices=market_prices,
        alpha=alpha,
        N=N,
        B=B,
        bounds=bounds,
        method=method,
        tol=tol,
        options=options,
    )
    
    summary = calibration_error_summary(
        calibrated_params=params,
        K=K,
        T=T,
        S0=S0,
        market_prices=market_prices,
        alpha=alpha,
        N=N,
        B=B,
    )

    return {
        "params": {
            "v0": params.v0,
            "r": params.r,
            "kappa": params.kappa,
            "theta": params.theta,
            "rho": params.rho,
            "xi": params.xi,
        },
        "market_prices": summary["market_prices"],
        "model_prices": summary["model_prices"],
        "abs_errors": summary["abs_errors"],
        "rmse": summary["rmse"],
        "loss": _loss,
        "success": _success,
        "message": _message, 
    }