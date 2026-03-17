from typing import Any
from fastapi import APIRouter, Query

from app.services.brownian import (
    simulate_brownian_motion,
    simulate_correlated_brownian_motion
)
from app.services.gbm import (
    simulate_gbm_paths,
    simulate_gbm_antihetic,
    simulate_gbm_euler
) 
from app.services.heston import simulate_heston_paths


router = APIRouter(prefix="/simulation", tags=["simulation"])


def _as_list(payload: Any) -> Any:
    if isinstance(payload, tuple):
        return [_as_list(item) for item in payload]
    if hasattr(payload, "tolist"):
        return payload.tolist()
    return payload


@router.post("/brownian")
def simulate_brownian(
    n_steps: int = Query(..., gt=1),
    n_paths: int = Query(..., gt=0),
    T: float = Query(..., gt=0),
    seed: int | None = Query(default=None)
) -> dict[str, Any]:
    W, dW = simulate_brownian_motion(n_steps, n_paths, T, seed)
    return {"W": _as_list(W), "dW": _as_list(dW)}


@router.post("/correlated_brownian")
def simulate_corr_brownian(
    rho: float = Query(..., ge=-1.0, le=1.0),
    n_steps: int = Query(..., gt=1),
    n_paths: int = Query(..., gt=0),
    T: float = Query(..., gt=0),
    seed: int | None = Query(default=None)
) -> dict[str, Any]:
    W1, W2, dW1, dW2 = simulate_correlated_brownian_motion(rho, n_steps, n_paths, T, seed)
    return {
        "W1": _as_list(W1),
        "W2": _as_list(W2),
        "dW1": _as_list(dW1),
        "dW2": _as_list(dW2)
    }


@router.post("/gbm_price")
def simulate_gbm_price_paths(
    S0: float,
    mu: float,
    sigma:  float = Query(..., ge=0),
    T: float = Query(..., gt=0),
    n_steps: int = Query(..., gt=1),
    n_paths: int = Query(..., gt=0),
    seed: int | None = Query(default=None)
) -> dict[str, Any]:
    paths = simulate_gbm_paths(S0, mu, sigma, T, n_steps, n_paths, seed)
    return {"paths": _as_list(paths)}


@router.post("/antihetic_gbm_price")
def simulate_antihetic_gbm_price_paths(
    S0: float,
    mu: float,
    sigma: float = Query(..., ge=0),
    T: float = Query(..., gt=0),
    n_steps: int = Query(..., gt=1),
    n_paths: int = Query(..., gt=0),
    seed: int | None = Query(default=None)
) -> dict[str, Any]:
    paths = simulate_gbm_antihetic(S0, mu, sigma, T, n_steps, n_paths, seed)
    return {"paths": _as_list(paths)}


@router.post("/gbm_euler_price")
def simulate_euler_gbm_price_paths(
    S0: float,
    mu: float,
    sigma: float = Query(..., ge=0),
    T: float = Query(..., gt=0),
    n_steps: int = Query(..., gt=1),
    n_paths: int = Query(..., gt=0),
    seed: int | None = Query(default=None)
) -> dict[str, Any]:
    paths = simulate_gbm_euler(S0, mu, sigma, T, n_steps, n_paths, seed)
    return {"paths": _as_list(paths)}



@router.post("/heston")
def simulate_heston_price_paths(
    S0: float,
    v0: float,
    rho: float = Query(..., ge=-1.0, le=1.0),
    T: float = Query(..., gt=0),
    n_steps: int = Query(..., gt=1),
    n_paths: int = Query(..., gt=0),
    mu: float = Query(...),
    theta: float = Query(..., ge=0),
    kappa: float = Query(..., ge=0),
    xi: float = Query(..., ge=0),
    seed: int | None = Query(default=None)
) -> dict[str, Any]:
    St, vt = simulate_heston_paths(S0, v0, rho, T, n_steps, n_paths, mu, theta, kappa, xi, seed)
    return {
        "St": _as_list(St),
        "vt": _as_list(vt)
    }