from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..db.models.propertyNegotiation import PropertyNegotiationModel
from .schema import PropertyNegotiation, PropertyResponse, RiskAssessment


def create_property_negotiation_service(
    db: Session, property: PropertyNegotiation
) -> PropertyResponse:
    # Assess the risk for the property negotiation
    risk_assessment = assess_risk(property)

    # Create the property negotiation entry in the database
    db_property = PropertyNegotiationModel(
        property_name=property.property_name,
        property_value=property.property_value,
        client_credit_score=property.client_credit_score,
        client_monthly_income_in_cents=property.client_monthly_income_in_cents,
        approved=risk_assessment.approved,
        reason=risk_assessment.reason,
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)

    return PropertyResponse(
        id=db_property.id,
        property_name=db_property.property_name,
        property_value=db_property.property_value,
        client_credit_score=db_property.client_credit_score,
        client_monthly_income_in_cents=db_property.client_monthly_income_in_cents,
        approved=risk_assessment.approved,
        reason=risk_assessment.reason,
    )


# Helper function for risk assessment
def assess_risk(property: PropertyNegotiation) -> RiskAssessment:
    if property.property_value > 10000000 or property.property_value < 100000:
        return RiskAssessment(
            approved=False, reason="Property value is outside acceptable range."
        )
    if property.client_credit_score < 500:
        return RiskAssessment(approved=False, reason="Credit score is too low.")
    if property.property_value > property.client_monthly_income_in_cents * 12 * 0.3:
        return RiskAssessment(
            approved=False, reason="Property value exceeds 30% of annual income."
        )
    return RiskAssessment(approved=True, reason="Approved")


def get_property_negotiation_service(id: int, db: Session) -> PropertyResponse:
    property_negotiation = (
        db.query(PropertyNegotiationModel)
        .filter(PropertyNegotiationModel.id == id)
        .first()
    )
    if not property_negotiation:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyResponse(
        id=property_negotiation.id,
        property_name=property_negotiation.property_name,
        property_value=property_negotiation.property_value,
        client_credit_score=property_negotiation.client_credit_score,
        client_monthly_income_in_cents=property_negotiation.client_monthly_income_in_cents,
        approved=property_negotiation.approved,
        reason=property_negotiation.reason,
    )
