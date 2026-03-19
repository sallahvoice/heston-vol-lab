from fastapi import APIRouter

from app.utils.misc import _as_list

from app.services.fft_pricing import carr_madan_fft_price
from app.services.monte_carlo import monte_carlo_european_call, monte_carlo_european_put

from app.schemas.pricing import (
    CarrMadanRequest, CarrMadanResponse,
    MonteCarloRequest, MonteCarloResponse
)

router = APIRouter(prefix="/pricing", tags=["pricing"])

@router.post("/monte_carlo_call", response_model=MonteCarloResponse)
def monte_carlo_call_pricing(req: MonteCarloRequest) -> MonteCarloResponse:
    return {"price": monte_carlo_european_call(req.St, req.K, req.r, req.T)}


@router.post("/monte_carlo_put", response_model=MonteCarloResponse)
def monte_carlo_put_pricing(req: MonteCarloRequest) -> MonteCarloResponse:
    return {"price": monte_carlo_european_put(req.St, req.K, req.r, req.T)}


@router.post("/carr_madan", response_model=CarrMadanResponse)
def carr_madan_pricing(req: CarrMadanRequest) -> CarrMadanResponse:
    k, C_k = carr_madan_fft_price(req.params, req.T, req.S0, req.alpha, req.N, req.B)
    return {
        "k": _as_list(k),
        "C_k": _as_list(C_k)
    }