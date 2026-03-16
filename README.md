#kalman filter (model vs real data observed)
#a garch model for auto-correlation (compare it to a heston model)

#todolist
2-app/api/v1/endpoints/simulation.py
Role: HTTP interface for your simulation engines (GBM/Heston path generation), using existing service layer functions.

3-app/api/v1/endpoints/pricing.py
Role: Pricing endpoints (Monte Carlo / FFT pricing requests and responses), acting as adapter over services/*.

4-app/api/v1/endpoints/calibration.py
Role: Calibration endpoint(s) to fit model parameters from market data and return diagnostics.

5-app/main.py
Role: FastAPI application bootstrap (app = FastAPI(...)), include v1 router, startup/shutdown hooks, middleware wiring.

6-app/api/v1/router.py
Role: Single place that mounts endpoint modules (health, simulation, pricing, calibration) under versioned prefix like /api/v1.

7-app/schemas/simulation.py
Role: Pydantic request/response models for simulation inputs/outputs (validation + OpenAPI docs).

8-app/schemas/pricing.py
Role: Pydantic models for pricing requests/results (strike, maturity, params, price, errors/confidence).

9-app/schemas/base.py
Role: Shared schema primitives (common config, pagination/meta/error envelope, reusable numeric constraints).



