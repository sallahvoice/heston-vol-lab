import numpy as np
from fastapi import APIRouter
from app.services.brownian import (simulate_brownian_motion, simulate_correlated_brownian_motion)
from app.services.gbm import simulate_gbm_paths, simulate_gbm_antihetic, simulate_gbm_euler 
from app.services.heston import simulate_heston_paths


router = APIRouter(prefix="simulation", tags=["simulation"])


@router.post("/brownian")
def simulate_brownian(
    n_steps: int,
    n_paths: int,
    T: float,
    seed: int | None = None
) -> Tuple[np.ndarray, np.ndarray]:
    return simulate_brownian_motion(n_steps, n_paths, T, seed)


@router.post("/correlated_brownian")
def simulate_corr_brownian(
    rho,
    n_steps: int,
    n_paths: int,
    T: float,
    seed: int | None = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return simulate_correlated_brownian_motion(rho, n_steps, n_paths, T, seed)


@router.post("/gbm_price")
def simulate_gbm_price_paths(
    S0: float,
    mu: float,
    sigma:  float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None
) -> np.ndarray:
    return simulate_gbm_paths(S0, mu, sigma, T, n_steps, n_paths, seed)


@router.post("/antihetic_gbm_price")
def simulate_antihetic_gmb_price_paths(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None
) -> np.ndarray:
    return simulate_gbm_antihetic(S0, mu, sigma, T, n_steps, n_paths, seed)


@router.post("/gmb_euler_price")
def simulate_euler_gbm_price_paths(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    n_steps: int,
    n_paths: int,
    seed: int | None = None
) -> np.ndarray:
    return simulate_gbm_euler(S0, mu, sigma, T, n_steps, n_paths, seed)



@router.post("/heston")
def simulate_heston_price_paths(
    S0: float,
    v0: float,
    rho: float,
    T: float,
    n_steps: int,
    n_paths: int,
    mu: float,
    theta: float,
    kappa: float,
    xi: float,
    seed: int | None = None
) -> tuple[np.ndarray, np.ndarray]:
    return simulate_heston_paths(S0, v0, rho, T, n_steps, n_paths, mu, theta, kappa, xi, seed)