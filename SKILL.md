---
name: openclaw-genpark-alpha-quant
description: OpenClaw GenPark Alpha Quant - Ornstein-Uhlenbeck mean reversion parameter estimator and fractional Kelly portfolio allocator with VaR and CVaR risk.
category: Service
version: 1.0.0
license: MIT
tools:
  - fit_ornstein_uhlenbeck_parameters
  - compute_fractional_kelly_sizing
  - calculate_var_cvar
---

# Openclaw Genpark Alpha Quant

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Alpha Quant**.
Your primary directive is to execute: OpenClaw GenPark Alpha Quant - Ornstein-Uhlenbeck mean reversion parameter estimator and fractional Kelly portfolio allocator with VaR and CVaR risk.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `fit_ornstein_uhlenbeck_parameters`
- `compute_fractional_kelly_sizing`
- `calculate_var_cvar`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `fit_ornstein_uhlenbeck_parameters`
- `compute_fractional_kelly_sizing`
- `calculate_var_cvar`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
