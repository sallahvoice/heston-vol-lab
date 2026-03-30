from fastapi import APIRouter, Query

from app.utils.misc import _as_list
from app.utils.redis_client import build_cache_key, get_json, set_json

from app.services.fft_pricing import carr_madan_fft_price
from app.services.monte_carlo import monte_carlo_european_call, monte_carlo_european_put

from app.schemas.pricing import (
    CarrMadanRequest,
    CarrMadanResponse,
    MonteCarloRequest,
    MonteCarloResponse,
)

router = APIRouter(prefix="/pricing", tags=["pricing"])


def _stable_payload(model) -> dict[str, Any]:
    return model.model_dump(mode="json")


@router.post("/monte_carlo_call", response_model=MonteCarloResponse)
def monte_carlo_call_pricing(
    req: MonteCarloRequest,
    use_cache: bool = Query(default=True),
    cache_ttl_seconds: int = Query(default=300, ge=1, le=86400),
) -> MonteCarloResponse:
    payload = _stable_payload(req)
    cache_key = build_cache_key("pricing:monte_carlo:call", payload)

    if use_cache:
        cached = get_json(cache_key)
        if cached is not None:
            return cached

    price = monte_carlo_european_call(
        req.St,
        req.K,
        req.r,
        req.T
    )

    response = {"price": float(price)}

    if use_cache:
        set_json(cache_key, response, ttl_seconds=cache_ttl_seconds)

    return response


@router.post("/monte_carlo_put", response_model=MonteCarloResponse)
def monte_carlo_put_pricing(
    req: MonteCarloRequest,
    use_cache: bool = Query(default=True),
    cache_ttl_seconds: int = Query(default=300, ge=1, le=86400),
) -> MonteCarloResponse:
    payload = _stable_payload(req)
    cache_key = build_cache_key("pricing:monte_carlo:put", payload)

    if use_cache:
        cached = get_json(cache_key)
        if cached is not None:
            return cached

    price = monte_carlo_european_put(
        req.St,
        req.K,
        req.r,
        req.T
    )

    response = {"price": float(price)}

    if use_cache:
        set_json(cache_key, response, ttl_seconds=cache_ttl_seconds)

    return response



@router.post("/carr_madan", response_model=CarrMadanResponse)
def carr_madan_pricing(
    req: CarrMadanRequest,
    use_cache: bool = Query(default=True),
    cache_ttl_seconds: int = Query(default=300, ge=1, le=86400),
    ) -> CarrMadanResponse:
    payload = _stable_payload(req)
    cache_key = build_cache_key("pricing:carr_madan", payload)

    if use_cache:
        cached = get_json(cache_key)
        if cached is not None:
            return cached

    k, c_k = carr_madan_fft_price(req.params, req.T, req.S0, req.alpha, req.N, req.B)

    response = {"log_strikes": _as_list(k), "call_prices": _as_list(c_k)}

    if use_cache:
        set_json(cache_key, response, ttl_seconds=cache_ttl_seconds)

    return response