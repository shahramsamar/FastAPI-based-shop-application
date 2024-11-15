from fastapi import FastAPI
from database import database
from models import models
from routers import products, customers, orders
# from meta_tags .meta_tags import tags_metadata
from meta_tags.meta_tags import tags_metadata



app = FastAPI(
              title="shop Api ",
              description="this is a shop app with minimal usage",
              version="0.0.1",
              terms_of_service="https://ecample.com/terms",
              contact={
                  "name": "Shahram Samar",
                  "url":"https://shahramsamar.github.io/",
                  "email": "shahramsamar2010@gmail.com",
              },
              license_info={"name":"MIT"},
              openapi_tags=tags_metadata,
              docs_url="/",
            )



# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])