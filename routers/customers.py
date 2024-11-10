from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import database
from models import models
from schemas import schemas
from database.database import get_db
from typing import Optional



router = APIRouter()



@router.get("/",description="List of customers")
async def customer_list(search: Optional[str] = Query(None,description="search by name"),
                       db:Session = Depends(get_db)):
    result = db.query(models.Customer)
    if search:
        result = result.filter(models.Customer.name == search)  
    return result.all() 




@router.get("/{customer_id}",response_model=schemas.Customer)
async def customer_read(customer_id: int ,db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is  None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
    



@router.post('/', response_model=schemas.Customer)
async def customer_create(customer: schemas.CustomerCreate,db: Session = Depends(get_db)):
    db_customer = models.Customer(name=customer.name,
                                  email=customer.email)
    if db_customer:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        raise HTTPException(status_code=200, detail="Customer created successfully")
    
    raise HTTPException(status_code=404, detail="Customer  created failed")



@router.put("/{customer_id}", response_model=schemas.Customer)
async def customer_update(customer_id: int, customer: schemas.CustomerCreate,
                         db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not  db_customer:
            raise HTTPException(status_code=404, detail="existing customer")

    db_customer.name = customer.name
    db_customer.email = customer.email
    db.commit()
    db.refresh(db_customer)
    return db_customer

   


      
@router.delete("/{customer_id}", response_model=dict)
async def customer_delete(customer_id: int, db: Session = Depends(get_db)):
    
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    
    # If the product doesn't exist, raise a 404 error
    if not  db_customer :
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    
    raise HTTPException(status_code=200, detail="Customer deleted successfully")