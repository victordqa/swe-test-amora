from pydantic import BaseModel, Field
from typing_extensions import Annotated


class PropertyNegotiation(BaseModel):
    property_name: str
    property_value_in_cents: Annotated[int, Field(ge=0)]
    client_credit_score: Annotated[int, Field(ge=0, le=1000)]
    client_monthly_income_in_cents: int


class RiskAssessment(BaseModel):
    approved: bool
    reason: str


class PropertyNegotiationDb(PropertyNegotiation, RiskAssessment):
    pass


class PropertyResponse(PropertyNegotiationDb):
    id: int
