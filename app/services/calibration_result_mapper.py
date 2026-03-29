from app.schemas.pricing import HestonParams, Diagnostics, PricingResponse

def to_response_payload(
    params: HestonParams,
    summary: dict,
    diagnostics: dict | None = None
    ) -> PricingResponse:

    return PricingResponse(
        params=HestonParams(
            v0=params.v0,
            r=params.r,
            kappa=params.kappa,
            theta=params.theta,
            rho=params.rho,
            xi=params.xi
        ),
        market_prices=summary.get("market_prices", []),
        model_prices=summary("model_prices", []),
        abs_errors=summary("abs_errors", []),
        rmse=summary("rmse", 0.0),
        diagnostics=Diagnostics(calibration_logs=diagnostics or {}) 
    )