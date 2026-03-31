import numpy as np

from app.services.monte_carlo import (
    discount_payoff,
    monte_carlo_confidence_interval,
    monte_carlo_european_call,
    monte_carlo_european_put,
    monte_carlo_standard_error
)


def test_discount_payoff_and_standard_error():
    payoff = np.array([10.0, 15.0, 20.0])
    discounted = discount_payoff(payoff, r=0.04, T=1.0)

    assert np.allclose(discounted, np.exp(-0.04) * payoff)
    assert monte_carlo_standard_error(discounted) > 0


def test_european_call_put_prices_on_fixed_terminal_values():
    St = np.array(
        [
            [100.0, 100.0, 100.0],
            [120.0, 90.0, 80.0],
        ]
    )
    K = 100.0
    r = 0.0
    T = 1.0

    call = monte_carlo_european_call(St, K=K, r=r, T=T)
    put = monte_carlo_european_put(St, K=K, r=r, T=T)

    assert np.isclose(call, np.mean([20.0, 0.0, 0.0]))
    assert np.isclose(put, np.mean([0.0, 10.0, 20.0]))


def test_confidence_interval_decision_rule():
    assert monte_carlo_confidence_interval(CL=0.95, abs_error=0.1, se=0.2)
    assert not monte_carlo_confidence_interval(CL=0.95, abs_error=1, se=0.1)