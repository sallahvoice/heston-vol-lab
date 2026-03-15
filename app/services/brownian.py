import numpy as np
from typing import Tuple

def _build_brownian_paths(dW: np.ndarray) -> np.ndarray:
    if not isinstance(dW, np.ndarray):
        raise TypeError("dW must be a numpy array")
    if dW.ndim != 2:
        raise ValueError("dW must be 2D (time x paths)")

    n_paths = dW.shape[1]
    W0 = np.zeros((1, n_paths))

    return np.vstack([W0, np.cumsum(dW, axis=0)])

def simulate_brownian_motion(
    n_steps: int,
    n_paths: int,
    T: float,
    seed: int | None = None
    ) -> Tuple[np.ndarray, np.ndarray]:

    if not  isinstance(n_steps, int):
        raise TypeError("n_steps must be an integer")

    if not isinstance(T, (int, float)):
        raise TypeError("T must be numeric")

    if not isinstance(n_paths, int):
        raise TypeError("n_paths must be an integer")

    if seed is not None and not isinstance(seed, int):
        raise TypeError("seed must be an integer or None")

    if n_steps <= 1:
        raise ValueError("n_steps must be greater than 1")

    if T <= 0:
        raise ValueError("T must be strictly positive")
    
    if n_paths <= 0:
        raise ValueError("n_paths must be strictly positive")

    rng = np.random.default_rng(seed)

    dt = T / (n_steps - 1)
    
    dW = rng.normal(
        loc=0.0,
        scale=np.sqrt(dt),
        size=(n_steps - 1, n_paths)
    )
    
    W = _build_brownian_paths(dW)

    return W, dW


def simulate_correlated_brownian_motion(
    rho,
    n_steps: int,
    n_paths: int,
    T: float,
    seed: int | None = None
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    if not isinstance(rho, (int, float)):
        raise TypeError("rho must be numeric")

    if abs(rho) > 1:
        raise ValueError("rho must be between -1 and 1")
    
    rng = np.random.default_rng(seed)

    dt = T / (n_steps - 1)

    corr = np.array([
        [1, rho],
        [rho, 1]
    ])

    L = np.linalg.cholesky(corr)
    Z = rng.normal(
        loc=0.0,
        scale=np.sqrt(dt),
        size=(n_steps - 1, n_paths, 2)
        )

    dW =  Z @ L.T
    dW1 = dW[:, :, 0]
    dW2 = dW[:, :, 1]

    W1 = _build_brownian_paths(dW1)
    W2 = _build_brownian_paths(dW2)
    
    return W1, W2, dW1, dW2


def quadratic_brownian_motion_variation(W: np.ndarray) -> np.ndarray:

    if not isinstance(W, np.ndarray):
        raise TypeError("W must be a numpy array")

    if W.ndim != 2:
        raise ValueError("W must be 2D array (time x paths)")

    increments = np.diff(W, axis=0)
    return np.cumsum(increments ** 2, axis=0)