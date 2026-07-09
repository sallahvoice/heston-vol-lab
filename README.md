
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
