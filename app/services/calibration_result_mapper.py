from dataclasses import dataclass

@dataclass
class ConstraintResult:
    is_valid: bool
    penalty: float
    reasons: list[str]

    def evaluate_heston_constraints(v0, kappa, theta, rho, xi) -> ConstraintResult:
        reasons = []
        penalty = 0.0 
        if  not (-1.0 <= rho <= 1.0):
            reasons.append("rho out of bound")
            penalty += 1e6
        if 2 * kappa * theta <= xi**2:
            reasons.append("feller condtion violated")
            penalty += 1e6
        
        return ConstraintResult(is_valid=(penalty==0.0), penalty=penalty, reasons=reasons)
        