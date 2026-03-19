from fastapi import APIRouter

from app.utils.misc import _as_list

from app.services.calibration import calibrate_heston
from app.schemas.calibration import HestonCalibrationRequest, HestonCalibrationResponse

router = APIRouter(prefix="/calibration", tags=["calibration"])

@router.post("/heston_calibration", response_model=HestonCalibrationResponse)
def heston_calibration(req: HestonCalibrationRequest) -> HestonCalibrationResponse:

    result = calibrate_heston(
        initial_guess=req.initial_guess,
        K=req.K,
        T=req.T,
        S0=req.S0,
        market_prices=req.market_prices,
        alpha=req.alpha,
        N=req.N,
        B=req.B,
        method=req.method,
        tol=req.tol,
        bounds=req.bounds,
        options=req.options
    )
    
    return {
        "params": result["params"],
        "market_prices": _as_list(result["market_prices"]),
        "model_prices": _as_list(result["model_prices"]),
        "abs_errors": _as_list(result["abs_errrors"]),
        "rmse": result["rmse"]
    }