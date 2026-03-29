from fastapi import APIRouter, Depends, HTTPException, Query, Response, Status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.calibration import CalibrationRun
from app.repositories.calibration_repository import CalibrationRepository
from app.services.calibration import calibrate_heston
from app.utils.misc import _as_list

from app.schemas.calibration import (
    CalibrationRunListResponse,
    CalibrationRunResponse,
    HestonCalibrationRequest,
    HestonCalibrationResponse,
)

from app.schemas.common import PaginationMeta

router = APIRouter(prefix="/calibration", tags=["calibration"])

@router.post("/heston_calibration", response_model=HestonCalibrationResponse)
def heston_calibration(
    req: HestonCalibrationRequest,
    save_run: bool = Query(default=True),
    db: Session = Depends(get_db),
    ) -> HestonCalibrationResponse:

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
        options=req.options,
    )

    if save_run:
        repo = CalibrationRepository(db)
        run_model = CalibrationRun(
            method=req.method,
            inputs={
                "initial_guess": req.initial_guess.model_dump(),
                "K": req.K,
                "T": req.T,
                "S0": req.S0,
                "market_prices": req.market_prices,
                "alpha": req.alpha,
                "N": req.N,
                "B": req.B,
                "bounds": req.bounds,
                "options": req.options,
                "tol": req.tol,
            },
            params=result["params"],
            rmse=result["rmse"],
        )
        repo.create_run(run_model)
    
    return {
        "params": result["params"],
        "market_prices": _as_list(result["market_prices"]),
        "model_prices": _as_list(result["model_prices"]),
        "abs_errors": _as_list(result["abs_errors"]),
        "rmse": result["rmse"],
        "loss": result["loss"],
        "success": result["success"],
        "message": result["message"],
    }


@router.get("/runs/{run_id}", response_model=CalibrationRunResponse)
def get_calibration_run(run_id: int, db: Session = Depends(get_db)) -> CalibrationRunResponse:
    repo = CalibrationRepository(db)
    run = repo.get_run_by_id(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Calibration run {run_id} not found")
    
    return {
        "id": run.id,
        "method": run.method,
        "inputs": run.inputs,
        "params": run.params,
        "rmse": run.rmse,
        "created_at": run.created_at,
    }


@router.get("/runs", response_model=CalibrationRunListResponse)
def get_calibration_runs(
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    ) -> CalibrationRunListResponse:
    repo = CalibrationRepository(db)
    runs = repo.list_recent_runs(limit=limit, offset=offset)
    total = repo.count_runs()
    
    return {
        "runs": [
            {
                "id": run.id,
                "method": run.method,
                "inputs": run.inputs,
                "params": run.params,
                "rmse": run.rmse,
                "created_at": run.created_at,                
            }
            for run in runs
        ],
        "pagination": PaginationMeta(limit=limit, offset=offset, total=total)
    }


@router.delete("/runs/{run_id}", status_code=Status.HTTP_204_NO_CONTENT)
def delete_calibration_run(run_id: int, db: Session = Depends(get_db)) -> Response:
    repo = CalibrationRepository(db)
    deleted = repo.delete_run(run_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Calibration run {run_id} not found"
        )
    
    return Response(status_code=Status.HTTP_204_NO_CONTENT)