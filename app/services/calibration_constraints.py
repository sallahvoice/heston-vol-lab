

def to_response_payload(params, summary: dict, diagnostics: dict | None = None) -> dict:
    payload = {
        params: {
            "v0": params.v0,
            "r": params.r,
            "kappa": params.kappa,
            "theta": params.theta,
            "rho": params.rho,
            "xi": params.xi
        },
        market_prices: summary["market_prices"],
        model_prices: summary["model_prices"],
        abs_errors: summary["abs_errors"],
        rmse: summary["rmse"]
    }

    if diagnostics:
        payload["diagnostics"] = diagnostics
    
    return payload