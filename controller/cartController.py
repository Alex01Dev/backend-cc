from sqlalchemy.orm import Session
from models.cartModel import Cart
from models.productsModel import Product
from schemas.productSchemas import StatusProducto

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or product.status != StatusProducto.disponible.value:
        return None

    # Verificar stock
    if product.quantity < quantity:
        return None  # no hay suficientes unidades

    # Revisar si ya está en carrito → actualiza cantidad
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_cart(db: Session, user_id: int):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    result = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            result.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "image_url": product.image_url,
                "quantity": item.quantity
            })
    return result

def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        return {"message": "El producto no está en el carrito"}

    db.delete(cart_item)
    db.commit()

    return {"message": f"Producto {product_id} eliminado del carrito"}

def purchase_cart(db: Session, user_id: int):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    purchased = []
    skipped = []  # productos que no se pudieron comprar

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            skipped.append({"product_id": item.product_id, "reason": "Producto no existe"})
            db.delete(item)  # limpiar del carrito
            continue

        # No permitir comprar productos propios
        if product.created_by == user_id:
            skipped.append({"product_id": product.id, "reason": "Producto propio"})
            db.delete(item)
            continue

        # Verificar que el producto esté disponible
        if product.status != StatusProducto.disponible.value:
            skipped.append({"product_id": product.id, "reason": "Producto no disponible"})
            db.delete(item)
            continue

        # Verificar stock suficiente
        if product.quantity >= item.quantity:
            product.quantity -= item.quantity
            if product.quantity == 0:
                product.status = StatusProducto.agotado.value

            purchased.append({
                "product_id": product.id,
                "quantity": item.quantity
            })
            db.delete(item)  # limpiar carrito
        else:
            skipped.append({"product_id": product.id, "reason": "Stock insuficiente"})

    db.commit()
    return {"purchased": purchased, "skipped": skipped}
