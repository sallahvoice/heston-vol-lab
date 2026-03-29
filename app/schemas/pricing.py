from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class MonteCarloRequest(BaseModel):
    St: List[List[float]]
    K: float = Field(..., gt=0)
    r: float = Field(...)
    T: float = Field(..., gt=0)


class MonteCarloResponse(BaseModel):
    price: float = Field(..., ge=0)


class HestonParams(BaseModel):
    v0: float = Field(..., gt=0)
    r: float = Field(...)
    kappa: float = Field(..., ge=0)
    theta: float = Field(..., ge=0)
    rho: float = Field(..., ge=-1.0, le=1.0)
    xi: float = Field(..., ge=0)


class Diagnostics(BaseModel):
    calibration_logs: dict


class PricingResponse(BaseModel):
    params: HestonParams
    market_prices: List[float]
    model_prices: List[float]
    abs_errors: List[float]
    rmse: float
    diagnostics: Optional[Diagnostics] = None


class CarrMadanRequest(BaseModel):
    params: HestonParams
    T: float = Field(..., gt=0)
    S0: float = Field(..., gt=0)
    alpha: float= Field(default=1.5)
    N: int = Field(default=4096, gt=0)
    B: float= Field(default=1000, gt=0)


class CarrMadanResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    log_strikes : List[float]
    call_prices : List[float]