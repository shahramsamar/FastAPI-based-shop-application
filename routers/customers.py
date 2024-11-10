from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import database
from models import models
from schemas import schemas
from database.database import get_db



router = APIRouter()



@router.post('/', response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate,db: Session = Depends(get_db)):
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.get("/{customer_id}",response_model=schemas.Customer)
def read_customer(customer_id: int ,db: Session = Depends(get_db)):
    customer =db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is  None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
    