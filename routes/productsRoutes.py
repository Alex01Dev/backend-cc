from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import SessionLocal
from schemas.productSchemas import Product, ProductCreate
from controller import productController

product_router = APIRouter(prefix="/products", tags=["products"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post("/create", response_model=Product)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return productController.create_product(db, product)

@product_router.get("/get", response_model=list[Product])
def read_all(db: Session = Depends(get_db)):
    return productController.get_products(db)

@product_router.get("/{product_id}", response_model=Product)
def read_one(product_id: int, db: Session = Depends(get_db)):
    db_product = productController.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@product_router.put("/{product_id}", response_model=Product)
def update(product_id: int, updates: ProductCreate, db: Session = Depends(get_db)):
    updated = productController.update_product(db, product_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@product_router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    deleted = productController.delete_product(db, product_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Deleted successfully"}
