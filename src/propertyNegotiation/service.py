from .schema import PropertyNegotiation, RiskAssessment


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
