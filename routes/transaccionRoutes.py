from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.productsModel import Product
from models.usersModel import User
from config.jwt import get_current_user

transaction_router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@transaction_router.post("/buy")
def buy_product(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # No permitir comprar si el producto lo creó el mismo usuario
    if product.created_by == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes comprar tus propios productos")

    # Validar stock
    if product.quantity < quantity:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible")

    # Reducir stock
    product.quantity -= quantity
    if product.quantity == 0:
        product.status = "agotado"

    db.commit()
    db.refresh(product)

    return {
        "message": "Compra realizada con éxito",
        "producto": product.name,
        "restante": product.quantity
    }
