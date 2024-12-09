from sqlalchemy import Column, Integer, String

from ..database import Base


class PropertyNegotiation(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String, index=True)
    property_value = Column(Integer)
    client_credit_score = Column(Integer)
    client_monthly_income_in_cents = Column(Integer)
