from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(
    title="Property Negotiation API",
    description="This API allows you to manage property negotiations and perform risk assessments.",
    version="1.0.0"
)

# Mock database
mock_db: Dict[int, dict] = {}

# Pydantic models
class PropertyNegotiation(BaseModel):
    property_name: str
    property_value: int
    client_credit_score: int
    client_monthly_income_in_cents: int

class RiskAssessment(BaseModel):
    approved: bool
    reason: str

class PropertyResponse(PropertyNegotiation, RiskAssessment):
    id: int

# Helper function for risk assessment
def assess_risk(property: PropertyNegotiation) -> RiskAssessment:
    if property.property_value > 10000000 or property.property_value < 100000:
        return RiskAssessment(approved=False, reason="Property value is outside acceptable range.")
    if property.client_credit_score < 500:
        return RiskAssessment(approved=False, reason="Credit score is too low.")
    if property.property_value > property.client_monthly_income_in_cents * 12 * 0.3:
        return RiskAssessment(approved=False, reason="Property value exceeds 30% of annual income.")
    return RiskAssessment(approved=True, reason="Approved")

# Endpoint to create a new "property"
@app.post("/imoveis", response_model=PropertyResponse, summary="Create a new property negotiation", description="Create a new property negotiation and assess its risk based on given parameters.")
def create_property(property: PropertyNegotiation):
    new_id = len(mock_db) + 1
    risk_assessment = assess_risk(property)
    property_data = property.dict()
    property_data.update({"id": new_id, "approved": risk_assessment.approved, "reason": risk_assessment.reason})
    mock_db[new_id] = property_data
    return property_data

# Endpoint to get "property" details by ID
@app.get("/imoveis/{id}", response_model=PropertyResponse, summary="Get property negotiation details", description="Retrieve the details of a property negotiation and its risk assessment by ID.")
def get_property(id: int):
    property = mock_db.get(id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property
