from dataclasses import dataclass
import numpy as np
from app.services.heston import simulate_heston_paths

@dataclass
class HestonParams:
    v0: float
    r: float
    kappa: float
    theta: float
    rho: float
    xi: float


def build_fft_grid(
    N: int,
    B: float
    ) -> np.ndarray:

    eta = B / N
    u = np.arange(N) * eta
    
    return u
    

#Lru caching from functools?
def heston_characteristic_function(
    u: complex, 
    params: HestonParams,
    T: float,
    S0: float,
) -> complex:

    i = 1j

    v0 = params.v0
    r= params.r
    kappa = params.kappa
    theta = params.theta
    rho = params.rho
    xi = params.xi

    b = kappa - rho * xi * i * u

    d = np.sqrt(b**2 + xi**2 * (u**2 + i * u))

    g = (b - d) / (b + d)

    exp_dT = np.exp(-d * T)

    C = (r * i * u * T + (kappa * theta / xi**2) * ((b - d) * T - 2 * np.log((1 - g * exp_dT) / (1-g))))

    D = ((b- d) / xi**2) * ((1 - exp_dT) / (1 - g * exp_dT))

    return np.exp(C + D * v0 + i * u * np.log(S0)) 


def carr_madan_integrand(
    u: np.ndarray,
    params: HestonParams,
    T: float,
    S0: float,
    alpha: float = 1.5,
    ) -> np.ndarray:

    i = 1j
    
    phi = heston_characteristic_function(
        u - i * (alpha + 1),
        params,
        T,
        S0
    )

    numerator = phi

    denominator = (
        alpha**2
        + alpha
        - u**2
        + i * (2 * alpha + 1) * u
    )

    return numerator / denominator


def carr_madan_fft_price(
    params: HestonParams,
    T: float,
    S0: float,
    alpha: float=1.5,
    N: int=2**12,
    B: float=1000
) -> tuple[np.ndarray, np.ndarray]:

    u = build_fft_grid(N, B)
    eta = u[1] - u[0]

    lamda = 2 * np.pi / (N * eta)
    b = N * lamda / 2
    k = -b + np.arange(N) * lamda

    integrand = carr_madan_integrand(
        u,
        params,
        T,
        S0,
        alpha
    )

    n = np.arange(N)
    simpson_weight = (
        3 + (-1)**n - (n == 0)
        ) / 3

    shift = np.exp(1j * u * b)

    fft_input = integrand * simpson_weight * shift
    fft_values = np.fft.fft(fft_input) * eta

    C_k = (np.exp(-alpha * k) / np.pi) * np.real(fft_values)

    return k, C_k #prices for log(k), make sure to interpolate prices.