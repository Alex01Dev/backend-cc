import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.usersModel import User
from models.productsModel import Product
from models.interactionModel import Interaccion
from models.commentModel import Comment  # Asegúrate de que esta ruta sea correcta
from config.db import SessionLocal, engine

# Configuración para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Datos de ejemplo
user_names = [
    "Juan Pérez", "María García", "Carlos López", "Ana Martínez",
    "Luis Rodríguez", "Sofía Hernández", "Miguel González", "Elena Díaz"
]

user_emails = [
    "juan.perez@example.com", "maria.garcia@example.com", 
    "carlos.lopez@example.com", "ana.martinez@example.com",
    "luis.rodriguez@example.com", "sofia.hernandez@example.com",
    "miguel.gonzalez@example.com", "elena.diaz@example.com"
]

product_categories = [
    "Alimentos", "Tecnologia", "Ropa", "Hogar", 
    "Limpieza", "Salud", "Papeleria", "Otros"
]

product_names = [
    "Leche Orgánica", "Botella ecologica", "Camiseta Algodón Orgánico",
    "Jabón Natural", "Libro Sostenibilidad", "Bicicleta",
    "Taza de bambu", "Pan Integral", "Zapatos ecologicos",
    "pajillas Reciclables", "Bolsa Tela", "Champu Sólido"
]

sample_comments = [
    "Excelente producto, muy recomendable.",
    "Me encantó, volvería a comprarlo.",
    "Buena relación calidad-precio.",
    "No era lo que esperaba, pero funciona.",
    "Empaque ecológico, muy bien.",
    "Lo recibí a tiempo y en buen estado.",
    "Podría mejorar, pero cumple su función.",
    "Estoy satisfecho con la compra."
]

def hash_password(password: str):
    return pwd_context.hash(password)

def create_users(db: Session, count=8):
    users = []
    for i in range(count):
        user = User(
            username=user_names[i],
            email=user_emails[i],
            password=hash_password(f"Password{i+1}!"),
            status="Active",
            registration_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            update_date=None
        )
        users.append(user)
        db.add(user)
    db.commit()
    return users

def create_products(db: Session, count=12):
    products = []
    for i in range(count):
        product = Product(
            name=product_names[i],
            category=random.choice(product_categories),
            carbon_footprint=round(random.uniform(0.1, 10.0), 2),
            recyclable_packaging=random.choice([True, False]),
            local_origin=random.choice([True, False])
        )
        products.append(product)
        db.add(product)
    db.commit()
    return products

def create_interactions(db: Session, users, products, count_per_user=7):
    interaction_types = [1, 2, 3]  # 1: vista, 2: clic, 3: favorito
    for user in users:
        for _ in range(count_per_user):
            interaction = Interaccion(
                user_id=user.id,
                product_id=random.choice(products).id,
                interaction=random.choice(interaction_types),
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 29))
            )
            db.add(interaction)
    db.commit()

def create_comments(db: Session, users, products, comments_per_product=3):
    for product in random.sample(products, k=min(len(products), 6)):  # Solo 6 productos comentados
        for _ in range(comments_per_product):
            comment = Comment(
                user_id=random.choice(users).id,
                product_id=product.id,
                content=random.choice(sample_comments)
            )
            db.add(comment)
    db.commit()

def main():
    db = SessionLocal()
    
    try:
        print("Creando usuarios...")
        users = create_users(db)

        print("Creando productos...")
        products = create_products(db)

        print("Creando interacciones...")
        create_interactions(db, users, products)

        print("Creando comentarios...")
        create_comments(db, users, products)

        print("\nSeeder completado exitosamente!")
        print(f"Total usuarios creados: {len(users)}")
        print(f"Total productos creados: {len(products)}")
        print(f"Total interacciones creadas: {len(users)*7}")
        print(f"Total comentarios estimados: {min(len(products),6)*3}")
    except Exception as e:
        db.rollback()
        print(f"\nError en el seeder: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
