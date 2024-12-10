from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..db.models.propertyNegotiation import PropertyNegotiationModel
from .repo import create_property_negotiation, get_property_negotiation
from .schema import PropertyNegotiation, PropertyResponse, RiskAssessment


def create_property_negotiation_service(
    db: Session, property: PropertyNegotiation
) -> PropertyResponse:
    risk_assessment = assess_risk(property)
    db_property = PropertyNegotiationModel(
        property_name=property.property_name,
        property_value_in_cents=property.property_value_in_cents,
        client_credit_score=property.client_credit_score,
        client_monthly_income_in_cents=property.client_monthly_income_in_cents,
        approved=risk_assessment.approved,
        reason=risk_assessment.reason,
    )
    db_property = create_property_negotiation(db, db_property)

    return PropertyResponse(
        id=db_property.id,
        property_name=db_property.property_name,
        property_value_in_cents=db_property.property_value_in_cents,
        client_credit_score=db_property.client_credit_score,
        client_monthly_income_in_cents=db_property.client_monthly_income_in_cents,
        approved=risk_assessment.approved,
        reason=risk_assessment.reason,
    )


def get_property_negotiation_service(id: int, db: Session) -> PropertyResponse:
    property_negotiation = get_property_negotiation(db, id)
    if not property_negotiation:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyResponse(
        id=property_negotiation.id,
        property_name=property_negotiation.property_name,
        property_value_in_cents=property_negotiation.property_value_in_cents,
        client_credit_score=property_negotiation.client_credit_score,
        client_monthly_income_in_cents=property_negotiation.client_monthly_income_in_cents,
        approved=property_negotiation.approved,
        reason=property_negotiation.reason,
    )


def assess_risk(property: PropertyNegotiation) -> RiskAssessment:
    RESTRICTIONS = {
        "property_value_min": 100000 * 100,  # value in cents
        "property_value_max": 10000000 * 100,  # value in cents
        "credit_score_min": 500,
        "income_to_property_ratio": 0.3,
    }

    reasons = []

    if (
        property.property_value_in_cents > RESTRICTIONS["property_value_max"]
        or property.property_value_in_cents < RESTRICTIONS["property_value_min"]
    ):
        reasons.append("Property value is outside acceptable range")

    if property.client_credit_score < RESTRICTIONS["credit_score_min"]:
        reasons.append("Credit score is too low")

    if (
        property.property_value_in_cents
        > property.client_monthly_income_in_cents
        * 12
        * RESTRICTIONS["income_to_property_ratio"]
    ):
        reasons.append("Property value exceeds 30% of annual income")

    if reasons:
        return RiskAssessment(approved=False, reason=", ".join(reasons))

    return RiskAssessment(approved=True, reason="All requirements are met")
