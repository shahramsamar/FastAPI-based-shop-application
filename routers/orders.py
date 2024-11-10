from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import database
from models import models
from schemas import schemas
from database.database import get_db
from typing import Optional



router = APIRouter()




@router.get("/",description="List of orders")
async def order_list(search: Optional[int] = Query(None,description="search by id"),
                       db:Session = Depends(get_db)):
    result = db.query(models.Order)
    if search:
        result = result.filter(models.Order.id == search)  
    return result.all() 



@router.post("/", response_model=schemas.Order)
async def order_create(order: schemas.OrderCreate, db:Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    db_customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    
    if  not db_product : 
        raise HTTPException(status_code=404, detail="Product not found")
    if not db_customer :
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if db_product.quantity < order.quantity:
        raise HTTPException(status_code=400,detail='Not enough product in stock')
    
    db_order = models.Order(product_id=order.product_id, customer_id=order.customer_id, quantity=order.quantity)
    db_product.quantity -= order.quantity
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
    
    
@router.get("/{order_id}/", response_model=schemas.Order)
async def order_read(order_id: int, db:Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
            raise HTTPException(status_code=404, detail="Order not found")
    return order
 
 
  
@router.put("/{order_id}", response_model=schemas.OrderBase)
async def order_update(order_id: int, order: schemas.OrderBase,
                         db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.product_id = order.product_id
    db_order.customer_id = order.customer_id
    db_order.quantity = order.quantity
    db.commit()
    db.refresh(db_order)
    return db_order
    

   


      
@router.delete("/{order_id}", response_model=dict)
async def order_delete(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not  db_order :
        raise HTTPException(status_code=404, detail="order not found")
    
    db.delete(db_order)
    db.commit()
    
    raise HTTPException(status_code=200, detail="order deleted successfully")
       