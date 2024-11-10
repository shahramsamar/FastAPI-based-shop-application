from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import database
from models import models
from schemas import schemas
from database.database import get_db



router = APIRouter()

@router.post("/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db:Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    db_customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    
    # if db_product in None or db_customer in None:
    #     raise HTTPException(status_code=404, detail="Product or Customer  not found")
    
    if db_product.quantity < order.quantity:
        raise HTTPException(status_code=400,detail='Not enough product in stock')
    
    db_order = models.Order(product_id=order.product_id, customer_id=order.customer_id, quantity=order.quantity)
    db_product.quantity -= order.quantity
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
    
@router.get("/{order_id}/", response_model=schemas.Order)
async def read_order(order_id: int, db:Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
            raise HTTPException(status_code=404, detail="Order not found")
    return order
    