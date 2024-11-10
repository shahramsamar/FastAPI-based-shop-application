from fastapi import FastAPI
from database import database
from models import models
from routers import products, customers


# Initialize FastAPI application
app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])