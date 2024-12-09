from pydantic import BaseModel


class PropertyNegotiation(BaseModel):
    property_name: str
    property_value: int
    client_credit_score: int
    client_monthly_income_in_cents: int


class RiskAssessment(BaseModel):
    approved: bool
    reason: str


class PropertyNegotiationDb(PropertyNegotiation, RiskAssessment):
    pass


class PropertyResponse(PropertyNegotiation, RiskAssessment):
    id: int
