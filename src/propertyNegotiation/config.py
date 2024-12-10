from .schema import Restrictions

RESTRICTIONS = Restrictions(
    property_value_min_in_cents=100000 * 100,
    property_value_max_in_cents=10000000 * 100,
    credit_score_min=500,
    income_to_property_ratio=0.3,
)
