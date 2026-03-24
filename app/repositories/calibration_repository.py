from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.calibration import CalibrationRun

class CalibrationRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_run(self, run_model: CalibrationRun) -> CalibrationRun:
        self.db.add(run_model)
        self.db.commit()
        self.db.refresh(run_model)
        return run_model

    def get_run_by_id(self, run_id: int) -> CalibrationRun | None:
        return self.db.query(CalibrationRun).filter(CalibrationRun.id == run_id).first()


    def list_recent_runs(self, limit: int) -> Sequence[CalibrationRun]:
        return self.db.query(CalibrationRun).order_by(desc(CalibrationRun.created_at)).limit(limit).all()

    #potential calibration CRUD queries