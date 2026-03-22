from sqlalchemy import Column, Integer, Float, String, JSON, DateTime, func
from app.db.base import base


class CalibrationRun(base):
    __tablename__ = "calibration_runs"
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String(50), nullable=False)
    inputs = Column(JSON, nullable=False)
    params = Column(JSON, nullable=False)
    rmse = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())