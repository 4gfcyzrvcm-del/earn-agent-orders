import unittest
from unittest.mock import patch
import verify_trc20_payment as v

TX = "a" * 64

class PaymentVerificationTests(unittest.TestCase):
    def test_invalid_txid_rejected(self):
        with self.assertRaises(ValueError):
            v.check("bad", "20")
    def test_invalid_amount_rejected(self):
        with self.assertRaises(ValueError):
            v.check(TX, "-2")
    def test_no_transaction_not_verified(self):
        with patch.object(v, "get", return_value={"data": []}):
            self.assertFalse(v.check(TX, "20")["verified"])
    def test_success_without_transfer_not_verified(self):
        def response(path):
            if path.endswith("/events?limit=200"):
                return {"success": True, "data": []}
            return {"data": [{"txID": TX, "ret": [{"contractRet": "SUCCESS"}], "blockNumber": 123}]}
        with patch.object(v, "get", side_effect=response):
            self.assertFalse(v.check(TX, "20")["verified"])
    def test_matching_transfer_verified(self):
        def response(path):
            if path.endswith("/events?limit=200"):
                return {"success": True, "data": [{"event_name": "Transfer", "contract_address": v.USDT_CONTRACT,
                    "result": {"to": v.RECIPIENT, "value": "20000000"}}]}
            return {"data": [{"txID": TX, "ret": [{"contractRet": "SUCCESS"}], "blockNumber": 123}]}
        with patch.object(v, "get", side_effect=response):
            self.assertTrue(v.check(TX, "20")["verified"])

if __name__ == "__main__":
    unittest.main()
