import pytest

from src.propertyNegotiation.config import RESTRICTIONS
from src.propertyNegotiation.schema import PropertyNegotiation
from src.propertyNegotiation.service import assess_risk


@pytest.fixture
def valid_property():
    monthly_income_in_cents = 500000 * 100
    return PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=monthly_income_in_cents * 0.30,
        client_credit_score=600,
        client_monthly_income_in_cents=monthly_income_in_cents,
    )


def test_property_value_outside_range():
    property_data = PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=RESTRICTIONS.property_value_max_in_cents
        + 1,  # High value
        client_credit_score=RESTRICTIONS.credit_score_min,
        client_monthly_income_in_cents=20000 * 100,
    )
    result = assess_risk(property_data)
    assert result.approved == False
    assert "Property value is outside acceptable range" in result.reason

    property_data.property_value_in_cents = (
        RESTRICTIONS.property_value_min_in_cents - 1
    )  # Low value
    result = assess_risk(property_data)
    assert result.approved == False
    assert "Property value is outside acceptable range" in result.reason


def test_credit_score_too_low():
    property_data = PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=500000 * 100,
        client_credit_score=RESTRICTIONS.credit_score_min - 1,  # Low credit score
        client_monthly_income_in_cents=20000 * 100,
    )
    result = assess_risk(property_data)
    assert result.approved == False
    assert "Credit score is too low" in result.reason


def test_property_value_exceeds_income_ratio():
    monthly_income_in_cents = 20000 * 100

    property_data = PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=(
            RESTRICTIONS.income_to_property_ratio * monthly_income_in_cents
        )
        + 1,  # Exceeds X% of monthly income
        client_credit_score=600,
        client_monthly_income_in_cents=monthly_income_in_cents,
    )
    result = assess_risk(property_data)
    assert result.approved == False
    assert "Property value exceeds monthly income tolerance" in result.reason


def test_all_requirements_met(valid_property):
    result = assess_risk(valid_property)
    assert result.approved == True
    assert result.reason == "All requirements are met"
