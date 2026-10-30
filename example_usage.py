# -*- coding: utf-8 -*-
from client import OpenClawGenParkAlphaQuant

quant = OpenClawGenParkAlphaQuant()

# 1. Ornstein-Uhlenbeck Mean Reversion
spread_data = [1.2, 1.4, 1.1, 0.9, 0.7, 0.8, 1.0, 1.1, 0.95, 1.05]
ou = quant.fit_ornstein_uhlenbeck_parameters(spread_data, dt=1.0)
print(f"OU Parameter Fit:")
print(f"  Theta: {ou['mean_reversion_speed_theta']}, Mu: {ou['long_term_equilibrium_mu']}, Half-Life: {ou['half_life_periods']} periods")

# 2. Fractional Kelly Sizing
kelly = quant.compute_fractional_kelly_sizing(expected_return=0.18, risk_free_rate=0.04, variance=0.035, kelly_fraction=0.5)
print(f"\nKelly Sizing: Leverage = {kelly['recommended_position_leverage']}x ({kelly['allocation_posture']})")

# 3. VaR & CVaR Risk
historical_returns = [-0.04, -0.02, 0.01, 0.03, -0.05, 0.02, -0.01, 0.04, -0.06, 0.01, 0.02, -0.01]
var_res = quant.calculate_var_cvar(historical_returns, confidence_level=0.95)
print(f"\nRisk Metrics (95% Confidence): VaR = {var_res['value_at_risk_var']*100:.2f}%, CVaR = {var_res['conditional_var_cvar']*100:.2f}%")
