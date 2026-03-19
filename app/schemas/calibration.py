from pydantic import BaseModel, Field, model_validator

from app.schemas.pricing import HestonParams


class HestonCalibrationRequest(BaseModel):
    initial_guess: HestonParams
    K: list[float] = Field(..., min_length=1)
    T: list[float] = Field(..., min_length=1)
    S0: float = Field(..., gt=0)
    market_prices: list[float] = Field(..., min_length=1)
    method: str = Field(default="L-BFGS-B")
    tol: float = Field(default=1e-6)
    alpha: float = Field(default=1.5)
    N: int = Field(default=4096, gt=0)
    B: float = Field(default=1000, gt=0)
    bounds: list[tuple[float | None, float | None]] | None = None
    options: dict | None = None


    @model_validator(mode="after")
    def validate_quote_lengths(self) -> "HestonCalibrationRequest":
        n = len(self.market_prices)
        if len(self.K) != n or len(self.T) != n:
            raise ValueError("K, T, and market_prices must have the same length.")
        if any(k <= 0 for k in self.K):
            raise ValueError("All strikes K must be positive.")
        if any(t <= 0 for t in self.T):
            raise ValueError("All maturities T must be positive.")
        return self

class HestonCalibrationResponse(BaseModel):
    params: HestonParams
    market_prices: list[float]
    model_prices: list[float]
    abs_errors: list[float]
    rmse: float