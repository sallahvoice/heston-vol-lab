import numpy as np
from app.services.brownian import simulate_correlated_brownian_motion
from app.utils.math_utils import TimeGrid


def simulate_heston_paths(
    S0: float,
    v0: float,
    rho: float,
    T: float,
    n_steps: int,
    n_paths: int,
    mu: float,
    theta: float,
    kappa: float,
    xi: float,
    seed: int | None = None
) -> tuple[np.ndarray, np.ndarray]:

    grid = TimeGrid.generate_time_grid(n_steps=n_steps, T=T)
    dt = grid.dt

    _, _, dW1, dW2 = simulate_correlated_brownian_motion(
        rho=rho,
        n_steps=n_steps,
        n_paths=n_paths,
        T=T,
        seed=seed
    )

    vt = heston_variance_full_truncation(
        v0=v0,
        dW2=dW2,
        dt=dt,
        theta=theta,
        kappa=kappa,
        xi=xi
    )

    St = heston_price_update(
        S0=S0,
        mu=mu,
        vt=vt,
        dW1=dW1,
        dt=dt
    )

    return St, vt


def heston_variance_full_truncation(
    v0: float,
    dW2: np.ndarray,
    dt: float,
    theta: float,
    kappa: float,
    xi: float,
) -> np.ndarray:

    n_steps = dW2.shape[0] + 1
    n_paths = dW2.shape[1]

    vt = np.zeros((n_steps, n_paths))
    vt[0] = v0

    for t in range(n_steps - 1):

        vt_plus = np.maximum(vt[t], 0)

        vt[t + 1] = (
            vt[t]
            + kappa * (theta - vt_plus) * dt
            + xi * np.sqrt(vt_plus) * dW2[t]
        )

    return vt


def heston_price_update(
    S0: float,
    mu: float,
    vt: np.ndarray,
    dW1: np.ndarray,
    dt: float,
) -> np.ndarray:

    n_steps, n_paths = vt.shape

    St = np.zeros((n_steps, n_paths))
    St[0] = S0

    for t in range(n_steps - 1):

        vt_plus = np.maximum(vt[t], 0)

        St[t + 1] = St[t] * np.exp(
            (mu - 0.5 * vt_plus) * dt
            + np.sqrt(vt_plus) * dW1[t]
        )

    return St


def check_feller_condition(
    theta: float,
    kappa: float,
    xi: float
) -> bool:

    return 2 * kappa * theta > xi**2