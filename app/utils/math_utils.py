import numpy as np
from dataclasses import dataclass

@dataclass
class TimeGrid:
    dt: float
    time_grid: np.ndarray

    @staticmethod
    def generate_time_grid(n_steps: int, T: float) -> "TimeGrid":

        if not  isinstance(n_steps, int):
            raise TypeError("n_steps must be an integer")

        if not isinstance(T, (int, float)):
            raise TypeError("T must be numeric")

        if n_steps <= 1:
            raise ValueError("n_steps must be greater than 1")

        if T <= 0:
            raise ValueError("T must be strictly positive")

        dt = T / (n_steps - 1)
        lines = np.linspace(0.0, T, n_steps)
        return TimeGrid(dt=dt, time_grid=lines)


def log_returns(values: np.ndarray) -> np.ndarray:
    return np.log(values[1:]) - np.log(values[:-1])