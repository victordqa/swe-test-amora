from typing import Dict

from fastapi import APIRouter, HTTPException

from .schema import PropertyNegotiation, PropertyResponse
from .service import assess_risk

propertyNegotiationRouter = APIRouter()

# Mock database
mock_db: Dict[int, dict] = {}


# Endpoint to create a new "property"
@propertyNegotiationRouter.post(
    "/",
    response_model=PropertyResponse,
    summary="Create a new property negotiation",
    description="Create a new property negotiation and assess its risk based on given parameters.",
)
def create_property(property: PropertyNegotiation):
    new_id = len(mock_db) + 1
    risk_assessment = assess_risk(property)
    property_data = property.dict()
    property_data.update(
        {
            "id": new_id,
            "approved": risk_assessment.approved,
            "reason": risk_assessment.reason,
        }
    )
    mock_db[new_id] = property_data
    return property_data


# Endpoint to get "property" details by ID
@propertyNegotiationRouter.get(
    "/{id}",
    response_model=PropertyResponse,
    summary="Get property negotiation details",
    description="Retrieve the details of a property negotiation and its risk assessment by ID.",
)
def get_property(id: int):
    property = mock_db.get(id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property
