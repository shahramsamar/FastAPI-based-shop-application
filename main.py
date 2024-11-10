from fastapi import FastAPI
from database import database
from models import models
from routers import products

# Initialize FastAPI application
app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(products.router, prefix="/products", tags=["products"])