import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.usersModel import User
from models.productsModel import Product
from models.interactionModel import Interaccion
from models.commentModel import Comment
from config.db import SessionLocal, engine, Base
from typing import List
from sqlalchemy import text

# Configuración para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Seeder:
    def __init__(self):
        self.db = SessionLocal()
        self.user_data = [
            {"username": "Juan Pérez", "email": "juan.perez@example.com"},
            {"username": "María García", "email": "maria.garcia@example.com"},
            {"username": "Carlos López", "email": "carlos.lopez@example.com"},
            {"username": "Ana Martínez", "email": "ana.martinez@example.com"},
            {"username": "Luis Rodríguez", "email": "luis.rodriguez@example.com"},
            {"username": "Sofía Hernández", "email": "sofia.hernandez@example.com"},
            {"username": "Miguel González", "email": "miguel.gonzalez@example.com"},
            {"username": "Elena Díaz", "email": "elena.diaz@example.com"}
        ]
        
        self.product_data = [
            {"name": "Leche Orgánica", "category": "Alimentos"},
            {"name": "Botella ecologica", "category": "Hogar"},
            {"name": "Camiseta Algodón Orgánico", "category": "Ropa"},
            {"name": "Jabón Natural", "category": "Limpieza"},
            {"name": "Libro Sostenibilidad", "category": "Papeleria"},
            {"name": "Bicicleta", "category": "Tecnologia"},
            {"name": "Taza de bambu", "category": "Hogar"},
            {"name": "Pan Integral", "category": "Alimentos"},
            {"name": "Zapatos ecologicos", "category": "Ropa"},
            {"name": "Pajillas Reciclables", "category": "Hogar"},
            {"name": "Bolsa Tela", "category": "Ropa"},
            {"name": "Champu Sólido", "category": "Limpieza"}
        ]
        
        self.image_urls = [
            "https://images.unsplash.com/photo-1590080876434-bd4a8d8e071b",
            "https://images.unsplash.com/photo-1600185365522-5e0f9fa2badd",
            "https://images.unsplash.com/photo-1542831371-d531d36971e6",
            "https://images.unsplash.com/photo-1611095564981-0d4bfe9d1804"
        ]

        self.profile_pictures = [
            "https://randomuser.me/api/portraits/men/32.jpg",
            "https://randomuser.me/api/portraits/women/45.jpg",
            "https://randomuser.me/api/portraits/men/76.jpg",
            "https://randomuser.me/api/portraits/women/12.jpg"
        ]
        
        self.sample_comments = [
            "Excelente producto, muy recomendable.",
            "Me encantó, volvería a comprarlo.",
            "Buena relación calidad-precio.",
            "No era lo que esperaba, pero funciona.",
            "Empaque ecológico, muy bien.",
            "Lo recibí a tiempo y en buen estado.",
            "Podría mejorar, pero cumple su función.",
            "Estoy satisfecho con la compra."
        ]

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def clear_database(self):
        """Limpia todas las tablas y reinicia los contadores de ID"""
        try:
            print("🧹 Limpiando base de datos y reiniciando IDs...")
            
            # Desactivar verificación de claves foráneas temporalmente
            self.db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            
            # Limpiar tablas en el orden correcto (primero las que dependen de otras)
            tables = [
                "tbd_comments",
                "tbd_interactions",
                "tbb_products",
                "tbb_users"
            ]
            
            for table in tables:
                self.db.execute(text(f"TRUNCATE TABLE {table}"))
                print(f"✓ Tabla {table} truncada")
                
            # Reactivar verificación de claves foráneas
            self.db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            
            # Reiniciar los auto-incrementos
            for table in tables:
                self.db.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))
                print(f"✓ Auto-incremento de {table} reiniciado a 1")
            
            self.db.commit()
            print("✅ Base de datos completamente limpia y IDs reiniciados")
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error al limpiar la base de datos: {e}")
            raise

    def create_users(self) -> List[User]:
        try:
            users = []
            for i, user_info in enumerate(self.user_data):
                user = User(
                    username=user_info["username"],
                    email=user_info["email"],
                    profile_picture=random.choice(self.profile_pictures),
                    password=self.hash_password(f"Password{i+1}!"),
                    status="Active",
                    registration_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    update_date=datetime.utcnow() if random.random() > 0.5 else None
                )
                self.db.add(user)
                users.append(user)
            self.db.commit()
            print(f"✅ {len(users)} usuarios creados en tbb_users")
            return users
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error creando usuarios: {e}")
            raise

    def create_products(self) -> List[Product]:
        try:
            products = []
            for product_info in self.product_data:
                product = Product(
                    name=product_info["name"],
                    category=product_info["category"],
                    carbon_footprint=round(random.uniform(0.1, 10.0), 2),
                    recyclable_packaging=random.choice([True, False]),
                    local_origin=random.choice([True, False]),
                    image_url=random.choice(self.image_urls)
                )
                self.db.add(product)
                products.append(product)
            self.db.commit()
            print(f"✅ {len(products)} productos creados en tbb_products")
            return products
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error creando productos: {e}")
            raise

    def create_interactions(self, users: List[User], products: List[Product]) -> None:
        try:
            interaction_types = [1, 2, 3]  # 1: vista, 2: clic, 3: favorito
            total_interactions = 0
            
            for user in users:
                interactions_count = random.randint(5, 10)  # 5-10 interacciones por usuario
                for _ in range(interactions_count):
                    interaction = Interaccion(
                        user_id=user.id,
                        product_id=random.choice(products).id,
                        interaction=random.choice(interaction_types),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 29))
                    )
                    self.db.add(interaction)
                    total_interactions += 1
            
            self.db.commit()
            print(f"✅ {total_interactions} interacciones creadas en tbd_interactions")
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error creando interacciones: {e}")
            raise

    def create_comments(self, users: List[User], products: List[Product]) -> None:
        try:
            total_comments = 0
            products_to_comment = random.sample(products, k=min(len(products), 8))  # 8 productos con comentarios
            
            for product in products_to_comment:
                comments_count = random.randint(1, 4)  # 1-4 comentarios por producto
                for _ in range(comments_count):
                    comment = Comment(
                        user_id=random.choice(users).id,
                        product_id=product.id,
                        content=random.choice(self.sample_comments),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 29))
                    )
                    self.db.add(comment)
                    total_comments += 1
            
            self.db.commit()
            print(f"✅ {total_comments} comentarios creados en tbd_comments")
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error creando comentarios: {e}")
            raise

    def run(self):
        try:
            # Crear tablas si no existen
            Base.metadata.create_all(bind=engine)
            
            # Limpiar la base de datos completamente
            self.clear_database()
            
            print("\n Comenzando inserción de datos...")
            
            # Insertar datos
            users = self.create_users()
            products = self.create_products()
            self.create_interactions(users, products)
            self.create_comments(users, products)
            
            # Verificación final
            print("\n Seeder completado exitosamente!")
            print("\n Resumen de datos insertados:")
            print(f"- Usuarios: {self.db.query(User).count()}")
            print(f"- Productos: {self.db.query(Product).count()}")
            print(f"- Interacciones: {self.db.query(Interaccion).count()}")
            print(f"- Comentarios: {self.db.query(Comment).count()}")
            
        except Exception as e:
            print(f"\n Error crítico en el seeder: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.db.close()

if __name__ == "__main__":
    should_seed = False  # Cambia esto a False si no quieres ejecutar el seeder

    if should_seed:
        seeder = Seeder()
        seeder.run()
    else:
        print(" Seeder desactivado manualmente.")
