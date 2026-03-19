from pydantic import BaseModel, Field

from app.schemas.pricing import HestonParams

class HestonCalibrationRequest(BaseModel):
    initial_guess: HestonParams
    K: float = Field(..., gt=0)
    T: float = Field(..., gt=0)
    S0: float = Field(..., gt=0)
    market_prices: np.ndarray
    method: str = Field(default="L-BFGS-B")
    tol: float = Field(default=1e-6)
    alpha: float = Field(default=1.5)
    N: int = Field(default=4096)
    B: float = Field(default=1000)
    bounds = None
    options: dict = None

class HestonCalibrationResponse(BaseModel):
    params: HestonParams
    market_prices: list[float]
    model_prices: list[float]
    abs_errors: list[float]
    rmse: float 