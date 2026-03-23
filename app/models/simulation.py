from sqlalchemy import Column, Integer, Float, String, JSON, DateTime, func

from app.db.base import base


class SimulationRun(base):
    __tablename__ = "simulation_runs"
    id = Column(Integer, primary_key=True, index=True)
    simulation_type = Column(String(64), nullable=False, index=True)
    inputs = Column(JSON, nullable=False)
    outputs = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())