from pydantic import BaseModel, Field

class HestonParams(BaseModel):
    v0: float = Field(..., gt=0)
    r: float = Field(...)
    kappa: float = Field(..., ge=0)
    theta: float = Field(..., ge=0)
    rho: float = Field(..., ge=-1.0, le=1.0)
    xi: float = Field(..., ge=0)

class CarrMadanResponse(BaseModel):
    params: HestonParams
    T: float = Field(..., gt=0),
    S0: float = Field(..., gt=0),
    alpha: float= Field(default=1.5),
    N: int = Field(default=4096),
    B: float= Field(default=1000)

class CarrMadanRequest(BaseModel):
    k : list[float]
    C_k : list[float]