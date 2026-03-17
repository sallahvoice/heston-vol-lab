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








Pricing and calibration routes are not exposed via v1 router.
Your v1 router currently wires only health and simulation; there is no inclusion of pricing/calibration routers, so those APIs are effectively missing from the mounted API surface. 

API contracts are weak (no explicit request/response schemas).
Simulation endpoints accept many primitive query args and return dict[str, Any] payloads, which weakens validation, OpenAPI clarity, and client typing. You likely want Pydantic request/response models for each endpoint. 

Endpoints are using query params for compute-heavy POSTs rather than JSON bodies.
Current signatures imply query-style inputs; for POST simulation jobs, body models are usually more scalable and easier for clients (especially for nested/optional configs). 

No API-layer exception mapping strategy is visible.
Services can throw domain errors, but API routes do not translate them into consistent HTTP responses (HTTPException or global exception handlers). That means error semantics are incomplete at API boundary. Domain exceptions exist elsewhere, but no mapping is visible in the API layer. 

No dependency injection usage at endpoint level (auth/rate limit/db/session hooks).
Current API endpoints do not use Depends(...) for shared concerns. If your project intends auth, tracing, request context, or per-request resources, this is still missing in API routes. 

Health endpoint is minimal (liveness only).
It returns status/timestamp, but there’s no readiness signal for downstream dependencies (DB/Redis/service checks), version, uptime, etc., which are often expected in production APIs. 

App-level API metadata/versioning ergonomics are minimal.
You mount the router at /api/v1, but there’s no visible title/description/version metadata configuration on FastAPI app creation, which helps docs and API governance.