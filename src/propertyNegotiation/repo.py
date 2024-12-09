from sqlalchemy.orm import Session

from ..db.models.propertyNegotiation import PropertyNegotiationModel


def create_property_negotiation(
    db: Session, property: PropertyNegotiationModel
) -> PropertyNegotiationModel:
    db.add(property)
    db.commit()
    db.refresh(property)
    return property


def get_property_negotiation(db: Session, id: int) -> PropertyNegotiationModel:
    return (
        db.query(PropertyNegotiationModel)
        .filter(PropertyNegotiationModel.id == id)
        .first()
    )
