# ---- future updates ? ----
#kalman filter (model vs real data observed)
#a garch model for auto-correlation (compare it to a heston model)
# ------
# ------
1) tests/api/test_calibration_endpoint.py
Goal: Verify /api/v1/calibration/heston_calibration request/response contract end-to-end.

Why this first:

Your calibration endpoint now has several shaped fields (K, T, market_prices, options/bounds) and output arrays that should always serialize correctly.

Hint snippet

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_heston_calibration_happy_path():
    payload = {
        "initial_guess": {"v0":0.04,"r":0.01,"kappa":2.0,"theta":0.04,"rho":-0.7,"xi":0.5},
        "K":[90,100], "T":[0.5,1.0], "S0":100, "market_prices":[12,8]
    }
    r = client.post("/api/v1/calibration/heston_calibration", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert set(["params","market_prices","model_prices","abs_errors","rmse"]).issubset(body.keys())
2) tests/services/test_calibration_service.py
Goal: Unit-test calibration service helpers and error behavior (especially input validation and broadcasting).

Why:

You have explicit validation/broadcast logic and interpolation-based model quote mapping; these are perfect for deterministic unit tests.

Hint snippet

import pytest
from app.services.calibration import _validate_and_broadcast_inputs

def test_validate_lengths_mismatch():
    with pytest.raises(ValueError):
        _validate_and_broadcast_inputs([90,100], [1.0], [10,11,12])

def test_validate_scalar_broadcast():
    K, T, m = _validate_and_broadcast_inputs(100, [0.5,1.0], [8,10])
    assert len(K) == len(T) == len(m) == 2
3) tests/api/test_pricing_endpoints.py
Goal: Validate all pricing routes and response schemas (monte_carlo_call, monte_carlo_put, carr_madan).

Why:

Pricing endpoints are a high-churn area and rely on schema strictness/response key correctness, so endpoint tests catch regressions fast.

Hint snippet

def test_monte_carlo_call_response_shape(client):
    payload = {"St": [[100,100],[101,99]], "K":100, "r":0.01, "T":1.0}
    r = client.post("/api/v1/pricing/monte_carlo_call", json=payload)
    assert r.status_code == 200
    assert "price" in r.json()   # keep schema aligned
4) tests/api/test_simulation_endpoints.py
Goal: Smoke-test the simulation API paths (brownian, correlated_brownian, gbm_*, heston) and basic output dimensions.

Why:

These routes are parameter-heavy and call numeric routines; they benefit a lot from shape checks and status checks.

Hint snippet

def test_brownian_shapes(client):
    r = client.post("/api/v1/simulation/brownian", json={"n_steps": 10, "n_paths": 3, "T": 1.0})
    assert r.status_code == 200
    body = r.json()
    assert len(body["W"]) == 10
    assert len(body["W"][0]) == 3
5) tests/conftest.py
Goal: Centralize reusable fixtures (client, standard payload builders, numeric tolerance config).

Why:

You already expose app via FastAPI and include router with /api/v1, so a shared TestClient fixture will remove duplication everywhere.

Hint snippet

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
#
# Heston Vol Lab

FastAPI service for stochastic-volatility research workflows: Heston FFT pricing, Monte Carlo pricing, path simulation, and parameter calibration.

## Quick start

### 1) Prerequisites
- Python 3.10+
- PostgreSQL
- Redis (optional but recommended for API caching)

### 2) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3) Configure environment
Copy the example file and update values for your machine:
```bash
cp .env.example .env
```

Key variables:
- `APP_NAME`, `ENVIRONMENT`, `LOG_LEVEL`
- `DB_URL`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_POOL_NAME`, `DB_POOL_SIZE`
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PASSWORD`
- `API_KEY` (required in `prod`, optional in `dev`)

### 4) Run migrations
```bash
alembic upgrade head
```

### 5) Start API
```bash
uvicorn app.main:app --reload
```

API base URL: `http://127.0.0.1:8000/api/v1`

## Runbook

### Health checks
```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

### Calibration flow
1. Submit calibration request.
2. Optionally persist the run (`save_run=true`).
3. Retrieve with `/calibration/runs/{run_id}`.
4. List recent runs with `/calibration/runs`.

### Cache behavior
- Pricing endpoints support `use_cache` and `cache_ttl_seconds` query parameters.
- If Redis is unavailable, the API continues to serve uncached responses.

### Logging
- `LOG_LEVEL` controls application verbosity.
- Startup/shutdown lifecycle logs include app/environment metadata.

## Endpoint examples

### Monte Carlo call pricing
```bash
curl -X POST 'http://127.0.0.1:8000/api/v1/pricing/monte_carlo_call?use_cache=true' \
  -H 'Content-Type: application/json' \
  -d '{
    "St": [[100.0, 101.0], [99.0, 102.0]],
    "K": 100.0,
    "r": 0.01,
    "T": 1.0
  }'
```

### Carr-Madan FFT pricing
```bash
curl -X POST 'http://127.0.0.1:8000/api/v1/pricing/carr_madan' \
  -H 'Content-Type: application/json' \
  -d '{
    "params": {"v0": 0.04, "r": 0.01, "kappa": 1.5, "theta": 0.04, "rho": -0.7, "xi": 0.3},
    "T": 1.0,
    "S0": 100.0,
    "alpha": 1.5,
    "N": 4096,
    "B": 1000
  }'
```

### Heston calibration
```bash
curl -X POST 'http://127.0.0.1:8000/api/v1/calibration/heston_calibration?save_run=true' \
  -H 'Content-Type: application/json' \
  -d '{
    "initial_guess": {"v0": 0.04, "r": 0.01, "kappa": 1.5, "theta": 0.04, "rho": -0.7, "xi": 0.3},
    "K": [90, 100, 110],
    "T": [0.5, 1.0, 1.5],
    "S0": 100,
    "market_prices": [14.2, 9.8, 6.1]
  }'
```