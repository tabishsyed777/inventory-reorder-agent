POLICY = {"safety_days": 3, "target_days": 14}
FIELDS = ("on_hand", "daily_demand", "lead_days")


def validate(case):
    if not isinstance(case, dict) or set(case) != {"sku", *FIELDS}:
        raise ValueError("Expected sku, on_hand, daily_demand, and lead_days.")
    if not isinstance(case["sku"], str) or not case["sku"].strip():
        raise ValueError("sku must be a nonempty string.")
    if any(type(case[field]) is not int or case[field] < 0 for field in FIELDS):
        raise ValueError("Stock, demand, and lead time must be nonnegative integers.")
    return case


def assess(case, policy):
    demand = case["daily_demand"]
    reorder_point = demand * (case["lead_days"] + policy["safety_days"])
    target = reorder_point + demand * policy["target_days"]
    quantity = 0
    if demand > 0 and case["on_hand"] <= reorder_point:
        quantity = target - case["on_hand"]
    return {"sku": case["sku"], "reorder_point": reorder_point,
            "order_quantity": quantity}
