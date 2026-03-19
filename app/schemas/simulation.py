from pydantic import BaseModel, Field
from typing import Optional


class BrownianRequest(BaseModel):
    n_steps: int = Field(..., gt=1),
    n_paths: int = Field(..., gt=0),
    T: float = Field(..., gt=0),
    seed: Optional[int] = None

class BrownianResponse(BaseModel):
    W : list[list[float]]
    dW: list[list[float]]


class CorrelatedBrownianRequest(BaseModel):
    rho: float = Field(..., ge=-1.0, le=1.0)
    n_steps: int = Field(..., gt=1)
    n_paths: int = Field(..., gt=0)
    T: float = Field(..., gt=0)
    seed: Optional[int] = None

class CorrelatedBrownianResponse(BaseModel):
    W1: list[list[float]]
    W2: list[list[float]]
    dW1: list[list[float]]
    dW2: list[list[float]]


class GBMRequest(BaseModel):
    S0: float = Field(..., gt=0)
    mu: float = Field(...)
    sigma : float = Field(..., ge=0)
    T: float = Field(..., gt=0)
    n_steps: int = Field(..., gt=1)
    n_paths: int = Field(..., gt=0)
    seed: Optional[int] = None

class GMBResponse(BaseModel):
    paths : list[list[float]]


class HestonRequest(BaseModel):
    S0: float = Field(..., gt=0)
    v0: float = Field(..., gt=0)
    rho: float = Field(..., ge=-1.0, le=1.0)
    n_steps: int = Field(..., gt=1)
    n_paths: int = Field(..., gt=0)
    mu: float
    theta: float = Field(..., ge=0)
    kappa: float = Field(..., ge=0)
    xi: float = Field(..., ge=0)
    seed: Optional[int] = None

class HestonResponse(BaseModel):
    St: list[list[float]]
    vt: list[list[float]]