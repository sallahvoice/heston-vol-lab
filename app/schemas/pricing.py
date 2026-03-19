from pydantic import BaseModel, Field


class MonteCarloRequest(BaseModel):
    St: list[list[float]]
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

class CarrMadanRequest(BaseModel):
    params: HestonParams
    T: float = Field(..., gt=0)
    S0: float = Field(..., gt=0)
    alpha: float= Field(default=1.5)
    N: int = Field(default=4096)
    B: float= Field(default=1000)

class CarrMadanResponse(BaseModel):
    k : list[float]
    C_k : list[float]