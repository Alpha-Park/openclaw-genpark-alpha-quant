# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Alpha Quant - Ornstein-Uhlenbeck Mean Reversion & Fractional Kelly Portfolio Allocator
Standard Library only: math, typing.
Estimates Ornstein-Uhlenbeck mean-reversion speed theta and long-term equilibrium mu,
calculates fractional Kelly criterion leverage, and computes Value-at-Risk (VaR) and CVaR.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkAlphaQuant:
    def __init__(self, default_kelly_fraction: float = 0.5):
        self.default_kelly = default_kelly_fraction

    def fit_ornstein_uhlenbeck_parameters(self, time_series: List[float],
                                          dt: float = 1.0) -> Dict[str, Any]:
        """
        Estimates continuous-time OU parameters: dx_t = theta * (mu - x_t) dt + sigma * dW_t
        Via linear regression of differences: Delta x = a + b * x_t
        where theta = -b / dt, mu = -a / b, sigma = std_residuals / sqrt(dt)
        """
        n = len(time_series)
        if n < 5:
            return {"error": "Need at least 5 data points"}

        x_prev = time_series[:-1]
        x_curr = time_series[1:]
        dx = [c - p for p, c in zip(x_prev, x_curr)]

        # OLS regression: dx = a + b * x_prev
        mean_x = sum(x_prev) / len(x_prev)
        mean_dx = sum(dx) / len(dx)

        cov_x_dx = sum((x - mean_x) * (y - mean_dx) for x, y in zip(x_prev, dx))
        var_x = sum((x - mean_x) ** 2 for x in x_prev)

        b = cov_x_dx / max(1e-9, var_x)
        a = mean_dx - b * mean_x

        # Parameter derivation
        theta = -b / dt
        mu = -a / b if abs(b) > 1e-9 else mean_x

        # Residuals
        residuals = [y - (a + b * x) for x, y in zip(x_prev, dx)]
        res_var = sum(r * r for r in residuals) / max(1, len(residuals) - 2)
        sigma = math.sqrt(res_var / dt)

        # Half-life of mean reversion: t_half = ln(2) / theta
        half_life = math.log(2.0) / theta if theta > 0 else 9999.0
        is_mean_reverting = theta > 0

        return {
            "data_points_count": n,
            "mean_reversion_speed_theta": round(theta, 4),
            "long_term_equilibrium_mu": round(mu, 4),
            "volatility_sigma": round(sigma, 4),
            "half_life_periods": round(half_life, 2),
            "is_mean_reverting": is_mean_reverting,
            "current_spread_from_mu": round(time_series[-1] - mu, 4)
        }

    def compute_fractional_kelly_sizing(self, expected_return: float,
                                        risk_free_rate: float,
                                        variance: float,
                                        kelly_fraction: float = None) -> Dict[str, Any]:
        """
        Calculates optimal leverage fraction f* = c * (mu - r) / sigma^2
        Clamped to [0.0, 3.0] to prevent catastrophic leverage blowouts.
        """
        c = kelly_fraction if kelly_fraction is not None else self.default_kelly
        excess_return = expected_return - risk_free_rate
        var = max(1e-6, variance)

        full_kelly = excess_return / var
        fractional_kelly = c * full_kelly

        # Clamp leverage
        recommended_leverage = max(0.0, min(3.0, fractional_kelly))

        return {
            "expected_return": round(expected_return, 4),
            "risk_free_rate": round(risk_free_rate, 4),
            "excess_return": round(excess_return, 4),
            "variance": round(variance, 6),
            "full_kelly_leverage": round(full_kelly, 4),
            "fractional_multiplier": c,
            "recommended_position_leverage": round(recommended_leverage, 4),
            "allocation_posture": "LONG_LEVERAGED" if recommended_leverage > 1.0 else ("LONG_UNLEVERAGED" if recommended_leverage > 0 else "CASH_FLAT")
        }

    def calculate_var_cvar(self, returns: List[float],
                          confidence_level: float = 0.95) -> Dict[str, Any]:
        """
        Calculates historical Value-at-Risk (VaR) and Conditional Value-at-Risk (CVaR / Expected Shortfall).
        VaR is the alpha-percentile loss; CVaR is the conditional expectation of loss exceeding VaR.
        """
        if not returns:
            return {"error": "Empty returns vector"}

        sorted_returns = sorted(returns)
        n = len(sorted_returns)
        alpha = 1.0 - confidence_level

        # Index corresponding to alpha percentile
        cutoff_idx = max(0, min(n - 1, int(math.floor(alpha * n))))
        var_alpha = -sorted_returns[cutoff_idx]

        # CVaR: average of losses in the tail <= cutoff
        tail_losses = [-r for r in sorted_returns[:cutoff_idx + 1]]
        cvar_alpha = sum(tail_losses) / len(tail_losses) if tail_losses else var_alpha

        return {
            "confidence_level": confidence_level,
            "observations_count": n,
            "value_at_risk_var": round(max(0.0, var_alpha), 4),
            "conditional_var_cvar": round(max(0.0, cvar_alpha), 4),
            "worst_observed_drawdown": round(-min(sorted_returns), 4)
        }
