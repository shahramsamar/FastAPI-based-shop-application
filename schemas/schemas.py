from pydantic import BaseModel

# Base class for Product model. It defines the common fields that will be used for creating or reading product data.
class ProductBase(BaseModel):
    name: str  # Product name as a string.
    price: float  # Product price as a float.
    quantity: int  # Product quantity as an integer.

# ProductCreate inherits from ProductBase but doesn't add any new fields.
# It will be used when creating a new product.
class ProductCreate(ProductBase):
    pass  # No additional fields or logic needed.

# Product model used to return product data. It includes the 'id' field.
class Product(ProductBase):
    id: int  # Product ID as an integer (to identify the product in the database).

    # Pydantic configuration to work with ORM models (e.g., SQLAlchemy).
    # This allows Pydantic to automatically convert ORM model data to Pydantic models.
    class Config:
        orm_mode = True

# Base class for Customer model. It defines the common fields for creating or reading customer data.
class CustomerBase(BaseModel):
    name: str  # Customer name as a string.
    email: str  # Customer email as a string.

# CustomerCreate inherits from CustomerBase and doesn't add any new fields.
# It is used when creating a new customer.
class CustomerCreate(CustomerBase):
    pass  # No additional fields or logic needed.

# Customer model used to return customer data. It includes the 'id' field.
class Customer(CustomerBase):
    id: int  # Customer ID as an integer.

    # Pydantic configuration to work with ORM models.
    class Config:
        orm_mode = True

# Base class for Order model. It defines the common fields for creating or reading order data.
class OrderBase(BaseModel):
    product_id: int  # Product ID associated with the order.
    customer_id: int  # Customer ID associated with the order.
    quantity: int  # Quantity of the product in the order.

# OrderCreate inherits from OrderBase and doesn't add any new fields.
# It is used when creating a new order.
class OrderCreate(OrderBase):
    pass  # No additional fields or logic needed.

# Order model used to return order data. It includes the 'id' field and references the related product and customer models.
class Order(OrderBase):
    id: int  # Order ID as an integer.
    product: Product  # Product object associated with the order.
    customer: Customer  # Customer object associated with the order.

    # Pydantic configuration to work with ORM models.
    class Config:
        orm_mode = True
