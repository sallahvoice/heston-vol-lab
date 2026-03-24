class CalibrationRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_run(self, run_model):
        self.db.add(run_model)
        self.db.commit()
        self.db.refresh(run_model)
        return run_model

    def list_recent_runs(self, limit):
        pass

    def get_calibration_by_id(self, id):
        pass

    def get_calibration_by_date(self, date):
        pass