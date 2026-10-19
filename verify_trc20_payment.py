#!/usr/bin/env python3
"""Check a TRON USDT TRC20 transfer using public TronGrid endpoints.

Read-only: no wallet keys, transfers, refunds or payment acceptance.
Requires transaction id and expected USDT amount. Network/API errors fail closed.
"""
import argparse
from decimal import Decimal, InvalidOperation
import json
import urllib.request

USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otL8n7k4d"
RECIPIENT = "THbFNVyz7iacnsA6sQkjgbtg6TCNjAjXBx"
BASE = "https://api.trongrid.io"

def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "earn-agent-payment-check/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)

def check(txid, expected):
    if len(txid) != 64 or any(c not in "0123456789abcdefABCDEF" for c in txid):
        raise ValueError("Transaction ID must be 64 hex characters")
    try:
        expected_units = int(Decimal(expected) * 1000000)
        if expected_units <= 0 or Decimal(expected) * 1000000 != expected_units:
            raise ValueError("Expected amount must be positive with at most 6 decimals")
    except InvalidOperation as exc:
        raise ValueError("Invalid USDT amount") from exc
    tx = get("/v1/transactions/" + txid)
    records = tx.get("data") or []
    if not records or not records[0].get("ret") or not any(x.get("contractRet") == "SUCCESS" for x in records[0]["ret"]):
        return {"verified": False, "reason": "Transaction missing or not successful"}
    if not records[0].get("blockNumber"):
        return {"verified": False, "reason": "No confirmed block"}
    events = get("/v1/transactions/" + txid + "/events?limit=200")
    total = 0
    for event in events.get("data") or []:
        result = event.get("result") or {}
        if (event.get("contract_address") == USDT_CONTRACT
                and event.get("event_name") == "Transfer"
                and result.get("to") == RECIPIENT):
            try:
                total += int(result.get("value", "0"))
            except (ValueError, TypeError):
                pass
    return {"verified": total >= expected_units, "observed_units": total,
            "expected_units": expected_units,
            "reason": "Matching confirmed transfer event" if total >= expected_units else "No matching sufficient transfer"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("txid", help="TRON transaction hash")
    parser.add_argument("expected_usdt", help="Expected amount, e.g. 20.00")
    args = parser.parse_args()
    try:
        result = check(args.txid, args.expected_usdt)
        print(json.dumps(result))
        raise SystemExit(0 if result["verified"] else 1)
    except Exception as exc:
        print(json.dumps({"verified": False, "reason": str(exc)}))
        raise SystemExit(1)
