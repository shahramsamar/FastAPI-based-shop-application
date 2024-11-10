from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from database import database
from models import models
from schemas import schemas
from database.database import get_db
from typing import Optional



router = APIRouter()



@router.get("/",description="List of product")
async def product_list(search: Optional[str] = Query(None,description="search by name"),
                       db:Session = Depends(get_db)):
    result = db.query(models.Product)
    if search:
        result = result.filter(models.Product.name == search)  
    return result.all() 


@router.get("/{product_id}", response_model=schemas.Product)
async def product_read(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, 
                            detail="Product not found")
    return product



@router.post("/", response_model=schemas.Product)
async def product_create(product: schemas.ProductCreate,
                         db: Session = Depends(get_db)):
    db_product = models.Product(name=product.name, 
                                price=product.price, quantity=product.quantity)
    if db_product:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        raise HTTPException(status_code=200, detail="Product created successfully")
   
    raise HTTPException(status_code=404, detail="Product  created failed")






@router.put("/{product_id}", response_model=schemas.Product)
async def product_update(product_id: int,product: schemas.ProductBase,
                         db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product
    

   


      
@router.delete("/{product_id}", response_model=dict)
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    # Retrieve the product by ID
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    # If the product doesn't exist, raise a 404 error
    if not  db_product :
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete the product and commit the transaction
    db.delete(db_product)
    db.commit()
    
    raise HTTPException(status_code=200, detail="Product deleted successfully")
     