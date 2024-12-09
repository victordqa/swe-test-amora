from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db

from .schema import PropertyNegotiation, PropertyResponse
from .service import (
    create_property_negotiation_service,
    get_property_negotiation_service,
)

propertyNegotiationRouter = APIRouter()


@propertyNegotiationRouter.post("/", response_model=PropertyResponse)
def create_property_negotiation(
    property: PropertyNegotiation, db: Session = Depends(get_db)
):
    property_data = create_property_negotiation_service(db, property)
    return property_data


@propertyNegotiationRouter.get("/{id}", response_model=PropertyResponse)
def get_property_negotiation(id: int, db: Session = Depends(get_db)):
    propertyNegotiationItem = get_property_negotiation_service(id, db)
    return propertyNegotiationItem
