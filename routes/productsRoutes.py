from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from config.db import SessionLocal
from schemas.productSchemas import Product, ProductCreate
from controller import productController
from schemas.userSchemas import User
from config.jwt import get_current_user  # Importa tu función aquí
from services.cloudinary import upload_image, DEFAULT_IMAGE

product_router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post("/create", response_model=Product)
async def create(
    name: str = Form(...),
    category: str = Form(...),
    carbon_footprint: float = Form(...),
    recyclable_packaging: bool = Form(...),
    local_origin: bool = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Llama a upload_image que maneja internamente el default
    image_url = upload_image(image) if image else DEFAULT_IMAGE

    product_data = {
        "name": name,
        "category": category,
        "carbon_footprint": carbon_footprint,
        "recyclable_packaging": recyclable_packaging,
        "local_origin": local_origin,
        "image_url": image_url
    }
    
    return productController.create_product(db, product_data)


@product_router.get("/get", response_model=list[Product])
def read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protección JWT
):
    return productController.get_products(db)

@product_router.get("/{product_id}", response_model=Product)
def read_one(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protección JWT
):
    db_product = productController.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@product_router.put("/{product_id}", response_model=Product)
def update(
    product_id: int, 
    updates: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protección JWT
):
    updated = productController.update_product(db, product_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@product_router.delete("/{product_id}")
def delete(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protección JWT
):
    deleted = productController.delete_product(db, product_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Deleted successfully"}
