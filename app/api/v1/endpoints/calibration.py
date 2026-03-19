from fastapi import APIRouter

from app.utils.misc import _as_list

from app.services.calibration import calibrate_heston
from app.schemas.calibration import (HestonCalibrationRequest, HestonCalibrationResponse)

router = APIRouter(prefix="/calibration", tags=["calibration"])

@router.post("/heston_calibration", response_model=HestonCalibrationResponse)
def heston_calibration(req: HestonCalibrationRequest) -> HestonCalibrationResponse:
    result = calibrate_heston(req.initial_guess, req.K, req.T, req.S0, req.market_prices, req.alpha, req.B, req.method, req.tol, req.N, req.bounds.req.options)
    return result