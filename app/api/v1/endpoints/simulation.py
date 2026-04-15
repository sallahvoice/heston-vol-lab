import numpy as np
from fastapi import APIRouter

from app.utils.misc import _as_list

from app.schemas.simulation import (
    BrownianRequest,
    BrownianResponse,
    CorrelatedBrownianRequest,
    CorrelatedBrownianResponse,
    GBMRequest,
    GBMResponse,
    HestonRequest,
    HestonResponse,
    HestonSummaryResponse,
)

from app.services.brownian import (
    simulate_brownian_motion,
    simulate_correlated_brownian_motion,
)
from app.services.gbm import (
    simulate_gbm_paths,
    simulate_gbm_antihetic,
    simulate_gbm_euler,
) 
from app.services.heston import simulate_heston_paths


router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.post("/brownian", response_model=BrownianResponse)
def simulate_brownian(req: BrownianRequest) -> BrownianResponse:
    W, dW = simulate_brownian_motion(req.n_steps, req.n_paths, req.T, req.seed)
    return {"W": _as_list(W), "dW": _as_list(dW)}


@router.post("/correlated_brownian", response_model=CorrelatedBrownianResponse)
def simulate_corr_brownian(req: CorrelatedBrownianRequest) -> CorrelatedBrownianResponse:
    W1, W2, dW1, dW2 = simulate_correlated_brownian_motion(
        req.rho, req.n_steps, req.n_paths, req.T, req.seed
    )
    return {
        "W1": _as_list(W1),
        "W2": _as_list(W2),
        "dW1": _as_list(dW1),
        "dW2": _as_list(dW2),
    }


@router.post("/gbm_price", response_model=GBMResponse)
def simulate_gbm_price_paths(req: GBMRequest) -> GBMResponse:
    paths = simulate_gbm_paths(
        req.S0, req.mu, req.sigma, req.T, req.n_steps, req.n_paths, req.seed
    )
    return {"paths": _as_list(paths)}


@router.post("/antihetic_gbm_price", response_model=GBMResponse)
def simulate_antihetic_gbm_price_paths(req: GBMRequest) -> GBMResponse:
    paths = simulate_gbm_antihetic(
        req.S0, req.mu, req.sigma, req.T, req.n_steps, req.n_paths, req.seed
    )
    return {"paths": _as_list(paths)}


@router.post("/gbm_euler_price", response_model=GBMResponse)
def simulate_euler_gbm_price_paths(req: GBMRequest) -> GBMResponse:
    paths = simulate_gbm_euler(
        req.S0, req.mu, req.sigma, req.T, req.n_steps, req.n_paths, req.seed
    )
    return {"paths": _as_list(paths)}



@router.post("/heston", response_model=HestonResponse)
def simulate_heston_price_paths(req: HestonRequest) -> HestonResponse:
    St, vt = simulate_heston_paths(
        req.S0,
        req.v0,
        req.rho,
        req.T,
        req.n_steps,
        req.n_paths,
        req.mu,
        req.theta,
        req.kappa,
        req.xi,
        req.seed
    )

    return {
        "St": _as_list(St),
        "vt": _as_list(vt)
    }


@router.post("/heston_summary", response_model=HestonSummaryResponse)
def simulate_heston_summary(req: HestonRequest) -> HestonSummaryResponse:
    St, vt = simulate_heston_paths(
        req.S0,
        req.v0,
        req.rho,
        req.T,
        req.n_steps,
        req.n_paths,
        req.mu,
        req.theta,
        req.kappa,
        req.xi,
        req.seed
    )

    summary = []
    for i in range(St.shape[0]):
        prices = St[i]
        vars_ = vt[i]
        summary.append(
            {
                "t": int(i),
                "mean_price": float(np.mean(prices)),
                "p05_prices": float(np.quantile(prices, 0.05)),
                "p95_prices": float(np.quantile(prices, 0.95)),
                "mean_variance": float(np.mean(vars_)),
            }
        )
    
    return {"summary": summary}