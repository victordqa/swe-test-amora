import pytest

from propertyNegotiation.schema import PropertyNegotiation
from propertyNegotiation.service import assess_risk


@pytest.fixture
def valid_property():
    return PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=5000000,
        client_credit_score=600,
        client_monthly_income_in_cents=200000,
    )


def test_property_value_outside_range():
    property_data = PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=2000000000,  # High value
        client_credit_score=600,
        client_monthly_income_in_cents=200000,
    )
    result = assess_risk(property_data)
    assert result.approved == False
    assert result.reason == "Property value is outside acceptable range."

    property_data.property_value_in_cents = 500000  # Low value
    result = assess_risk(property_data)
    assert result.approved == False
    assert result.reason == "Property value is outside acceptable range."


def test_credit_score_too_low():
    property_data = PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=5000000,
        client_credit_score=400,  # Low credit score
        client_monthly_income_in_cents=200000,
    )
    result = assess_risk(property_data)
    assert result.approved == False
    assert result.reason == "Credit score is too low."


def test_property_value_exceeds_income_ratio():
    property_data = PropertyNegotiation(
        property_name="Test Property",
        property_value_in_cents=8000000,  # Exceeds 30% of annual income
        client_credit_score=600,
        client_monthly_income_in_cents=200000,
    )
    result = assess_risk(property_data)
    assert result.approved == False
    assert result.reason == "Property value exceeds 30% of annual income."


def test_all_requirements_met(valid_property):
    result = assess_risk(valid_property)
    assert result.approved == True
    assert result.reason == "All requirements are met"