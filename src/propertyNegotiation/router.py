from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db

from .schema import PropertyNegotiation, PropertyResponse
from .service import create_property_negotiation_service

propertyNegotiationRouter = APIRouter()


@propertyNegotiationRouter.post("/", response_model=PropertyResponse)
def create_property(property: PropertyNegotiation, db: Session = Depends(get_db)):
    property_data = create_property_negotiation_service(db, property)
    return property_data


@propertyNegotiationRouter.get("/{id}", response_model=PropertyResponse)
def get_property(id: int, db: Session = Depends(get_db)):
    property = db.query(PropertyModel).filter(PropertyModel.id == id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property
