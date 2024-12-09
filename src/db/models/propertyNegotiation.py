from sqlalchemy import Boolean, Column, Integer, String

from ..database import Base


class PropertyNegotiationModel(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String, unique=True)
    property_value = Column(Integer)
    client_credit_score = Column(Integer)
    client_monthly_income_in_cents = Column(Integer)
    approved = Column(Boolean)
    reason = Column(String)
