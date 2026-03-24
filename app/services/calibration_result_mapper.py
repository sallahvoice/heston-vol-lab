from dataclasses import dataclass

PENALTY = 1e6
EPS = 1e-12

@dataclass
class ConstraintResult:
    is_valid: bool
    penalty: float
    reasons: list[str]


def evaluate_heston_constraints(
        v0: float,
        kappa: float,
        theta: float,
        rho: float,
        xi: float
    ) -> "ConstraintResult":
        reasons: list[str] = []
        penalty = 0.0 

        if v0 <= 0:
            reasons.append("v0 must be strictly positive")
            penalty += PENALTY

        if  not (-1.0 <= rho <= 1.0):
            reasons.append("rho out of bound")
            penalty += PENALTY
            
        if 2 * kappa * theta <= xi**2 + EPS:
            reasons.append("feller condition violated")
            penalty += PENALTY
        
        return ConstraintResult(is_valid= not reasons, penalty=penalty, reasons=reasons)
        