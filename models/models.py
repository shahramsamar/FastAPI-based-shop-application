from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base  # Import the Base class from the database module to use as a base for all models.

# Product model represents a product in the database.
# It maps to the 'products' table in the database.
class Product(Base):
    __tablename__ = "products"  # Specify the table name in the database.

    # Define the columns in the 'products' table:
    id = Column(Integer, primary_key=True, index=True)  # Primary key, automatically indexed for faster queries.
    name = Column(String, index=True)  # Product name, indexed for quick lookups.
    price = Column(Float)  # Product price, stored as a float.
    quantity = Column(Integer)  # Quantity of the product in stock.

# Customer model represents a customer in the database.
# It maps to the 'customers' table in the database.
class Customer(Base):
    __tablename__ = "customers"  # Specify the table name in the database.

    # Define the columns in the 'customers' table:
    id = Column(Integer, primary_key=True, index=True)  # Primary key, automatically indexed for faster queries.
    name = Column(String, index=True)  # Customer name, indexed for quick lookups.
    email = Column(String, unique=True, index=True)  # Customer email, unique and indexed to ensure no duplicates.

# Order model represents an order placed by a customer for a product.
# It maps to the 'orders' table in the database.
class Order(Base):
    __tablename__ = "orders"  # Specify the table name in the database.

    # Define the columns in the 'orders' table:
    id = Column(Integer, primary_key=True, index=True)  # Primary key, automatically indexed for faster queries.
    product_id = Column(Integer, ForeignKey("products.id"))  # Foreign key to the 'products' table.
    customer_id = Column(Integer, ForeignKey("customers.id"))  # Foreign key to the 'customers' table.
    quantity = Column(Integer)  # Quantity of the product in the order.

    # Define relationships to other models:
    product = relationship("Product")  # Establish a relationship to the Product model, automatically loading the related product.
    customer = relationship("Customer")  # Establish a relationship to the Customer model, automatically loading the related customer.
