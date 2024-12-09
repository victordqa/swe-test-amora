from fastapi import FastAPI

from src.db.database import engine
from src.db.models import propertyNegotiation
from src.propertyNegotiation.router import propertyNegotiationRouter

propertyNegotiation.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Property Negotiation API",
    description="This API allows you to manage property negotiations and perform risk assessments.",
    version="1.0.0",
)

app.include_router(propertyNegotiationRouter, prefix="/imoveis")
