from fastapi import APIRouter

from app.utils.misc import _as_list

from app.schemas.simulation import (
    BrownianRequest, BrownianResponse,
    CorrelatedBrownianRequest, CorrelatedBrownianResponse,
    GBMRequest, GMBResponse,
    HestonRequest, HestonResponse
)

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


@router.post("/brownian", response_model=BrownianResponse)
def simulate_brownian(req: BrownianRequest) -> BrownianResponse:
    W, dW = simulate_brownian_motion(n_steps, n_paths, T, seed)
    return {"W": _as_list(W), "dW": _as_list(dW)}


@router.post("/correlated_brownian", response_model=CorrelatedBrownianResponse)
def simulate_corr_brownian(req: CorrelatedBrownianRequest) -> CorrelatedBrownianResponse:
    W1, W2, dW1, dW2 = simulate_correlated_brownian_motion(rho, n_steps, n_paths, T, seed)
    return {
        "W1": _as_list(W1),
        "W2": _as_list(W2),
        "dW1": _as_list(dW1),
        "dW2": _as_list(dW2)
    }


@router.post("/gbm_price", response_model=GMBResponse)
def simulate_gbm_price_paths(req: GBMRequest) -> GMBResponse:
    paths = simulate_gbm_paths(S0, mu, sigma, T, n_steps, n_paths, seed)
    return {"paths": _as_list(paths)}


@router.post("/antihetic_gbm_price", response_model=GMBResponse)
def simulate_antihetic_gbm_price_paths(req: GBMRequest) -> GMBResponse:
    paths = simulate_gbm_antihetic(S0, mu, sigma, T, n_steps, n_paths, seed)
    return {"paths": _as_list(paths)}


@router.post("/gbm_euler_price", response_model=GMBResponse)
def simulate_euler_gbm_price_paths(req: GBMRequest) -> GMBResponse:
    paths = simulate_gbm_euler(S0, mu, sigma, T, n_steps, n_paths, seed)
    return {"paths": _as_list(paths)}



@router.post("/heston", response_model=HestonResponse)
def simulate_heston_price_paths(req: HestonRequest) -> HestonResponse:
    St, vt = simulate_heston_paths(S0, v0, rho, T, n_steps, n_paths, mu, theta, kappa, xi, seed)
    return {
        "St": _as_list(St),
        "vt": _as_list(vt)
    }