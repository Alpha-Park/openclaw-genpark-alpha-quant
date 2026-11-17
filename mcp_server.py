# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkAlphaQuant

client = OpenClawGenParkAlphaQuant()

TOOLS = [
    {
        "name": "fit_ornstein_uhlenbeck_parameters",
        "description": "Estimates continuous-time OU mean reversion speed, equilibrium mu, and half-life.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "time_series": {"type": "array", "items": {"type": "number"}},
                "dt": {"type": "number"}
            },
            "required": ["time_series"]
        }
    },
    {
        "name": "compute_fractional_kelly_sizing",
        "description": "Calculates optimal fractional Kelly leverage and position allocation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expected_return": {"type": "number"},
                "risk_free_rate": {"type": "number"},
                "variance": {"type": "number"},
                "kelly_fraction": {"type": "number"}
            },
            "required": ["expected_return", "risk_free_rate", "variance"]
        }
    },
    {
        "name": "calculate_var_cvar",
        "description": "Calculates historical Value-at-Risk (VaR) and Expected Shortfall (CVaR).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "returns": {"type": "array", "items": {"type": "number"}},
                "confidence_level": {"type": "number"}
            },
            "required": ["returns"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "fit_ornstein_uhlenbeck_parameters":
            res = client.fit_ornstein_uhlenbeck_parameters(args["time_series"], args.get("dt", 1.0))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_fractional_kelly_sizing":
            res = client.compute_fractional_kelly_sizing(args["expected_return"], args["risk_free_rate"], args["variance"], args.get("kelly_fraction"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "calculate_var_cvar":
            res = client.calculate_var_cvar(args["returns"], args.get("confidence_level", 0.95))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            try:
                req = json.loads(line)
            except json.JSONDecodeError as exc:
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}), flush=True)
                continue
            if not isinstance(req, dict) or req.get("jsonrpc") != "2.0" or not isinstance(req.get("method"), str):
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}), flush=True)
                continue
            # JSON-RPC notifications never receive a response or execute request-only tools.
            if "id" not in req:
                continue
            if req["method"] == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {
                    "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                    "serverInfo": {"name": 'openclaw-genpark-alpha-quant', "version": "1.0.0"}
                }}), flush=True)
                continue
            if req["method"] == "ping":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {}}), flush=True)
                continue
            if req["method"] not in ("tools/list", "tools/call"):
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32601, "message": "Method not found"}}), flush=True)
                continue
            if req["method"] == "tools/call":
                params = req.get("params")
                if not isinstance(params, dict) or not isinstance(params.get("arguments", {}), dict) or params.get("name") not in ('fit_ornstein_uhlenbeck_parameters', 'compute_fractional_kelly_sizing', 'calculate_var_cvar'):
                    print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32602, "message": "Unknown tool or invalid arguments"}}), flush=True)
                    continue
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req.get("id") if isinstance(req, dict) else None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
