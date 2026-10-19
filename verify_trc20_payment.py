#!/usr/bin/env python3
"""Read-only TRON USDT payment verification. Never authorizes delivery alone."""
import argparse
from decimal import Decimal, InvalidOperation
import json
import urllib.request

USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otL8n7k4d"
RECIPIENT = "THbFNVyz7iacnsA6sQkjgbtg6TCNjAjXBx"
BASE = "https://api.trongrid.io"
TRON_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def tron_hex(address):
    """Convert TRON Base58Check to 20-byte EVM-style address hex."""
    import hashlib
    n = 0
    for c in address:
        n = n * 58 + TRON_ALPHABET.index(c)
    data = n.to_bytes(25, "big")
    checksum = hashlib.sha256(hashlib.sha256(data[:21]).digest()).digest()[:4]
    if len(data) != 25 or data[0] != 0x41 or data[21:] != checksum:
        raise ValueError("Invalid TRON address")
    return data[1:21].hex()

def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "earn-agent-payment-check/2.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def check(txid, expected):
    if len(txid) != 64 or any(c not in "0123456789abcdefABCDEF" for c in txid):
        raise ValueError("Transaction ID must be 64 hex characters")
    try:
        units = Decimal(expected) * 1000000
        if not units.is_finite() or units <= 0 or units != int(units):
            raise ValueError("Expected amount must be positive with at most 6 decimals")
        expected_units = int(units)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Invalid USDT amount") from exc
    tx = get("/v1/transactions/" + txid)
    records = tx.get("data") or []
    if not records or records[0].get("txID", "").lower() != txid.lower():
        return {"verified": False, "reason": "Transaction not found"}
    record = records[0]
    if not any(x.get("contractRet") == "SUCCESS" for x in record.get("ret", [])):
        return {"verified": False, "reason": "Transaction unsuccessful"}
    if not record.get("blockNumber"):
        return {"verified": False, "reason": "Transaction not in confirmed block"}
    events = get("/v1/transactions/" + txid + "/events?limit=200")
    if not events.get("success", False):
        return {"verified": False, "reason": "Event lookup failed"}
    recipient_hex = tron_hex(RECIPIENT)
    contract_hex = tron_hex(USDT_CONTRACT)
    total = 0
    for event in events.get("data") or []:
        if event.get("event_name") != "Transfer":
            continue
        contract = event.get("contract_address", "")
        if contract != USDT_CONTRACT and contract.lower().removeprefix("41") != contract_hex:
            continue
        result = event.get("result") or {}
        target = str(result.get("to", ""))
        if target != RECIPIENT and target.lower().removeprefix("0x").removeprefix("41") != recipient_hex:
            continue
        try:
            amount = int(result.get("value", "0"))
            if amount > 0:
                total += amount
        except (TypeError, ValueError):
            continue
    return {"verified": total >= expected_units, "observed_units": total,
            "expected_units": expected_units, "txid": txid,
            "reason": "Matching successful confirmed transfer" if total >= expected_units else "No sufficient matching transfer"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("txid")
    parser.add_argument("expected_usdt")
    args = parser.parse_args()
    try:
        result = check(args.txid, args.expected_usdt)
        print(json.dumps(result))
        raise SystemExit(0 if result["verified"] else 1)
    except Exception as exc:
        print(json.dumps({"verified": False, "reason": str(exc)}))
        raise SystemExit(1)
