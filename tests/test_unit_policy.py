import unittest

from inventory_reorder_agent.policy import POLICY, assess, validate


class PolicyTests(unittest.TestCase):
    def test_stock_boundary(self):
        base = {"sku": "A", "daily_demand": 5, "lead_days": 2}
        self.assertEqual(assess(dict(base, on_hand=25), POLICY)["order_quantity"], 70)
        self.assertEqual(assess(dict(base, on_hand=26), POLICY)["order_quantity"], 0)

    def test_no_demand(self):
        case = {"sku": "A", "on_hand": 0, "daily_demand": 0, "lead_days": 3}
        self.assertEqual(assess(case, POLICY)["order_quantity"], 0)

    def test_invalid_quantity(self):
        for amount in (-1, True, 0.5, "5"):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                validate({"sku": "A", "on_hand": amount, "daily_demand": 1, "lead_days": 2})
