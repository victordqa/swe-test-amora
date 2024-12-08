from fastapi import FastAPI

from src.propertyNegotiation.router import propertyNegotiationRouter

app = FastAPI(
    title="Property Negotiation API",
    description="This API allows you to manage property negotiations and perform risk assessments.",
    version="1.0.0",
)

app.include_router(propertyNegotiationRouter, prefix="/imoveis")
