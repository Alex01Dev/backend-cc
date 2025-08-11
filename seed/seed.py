from sqlalchemy.orm import Session
from config.db import SessionLocal
from passlib.context import CryptContext
from faker import Faker
import random
from datetime import datetime, timedelta
from models.usersModel import User
from models.productsModel import Product
from models.interactionModel import Interaccion
from models.commentModel import Comment

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Seeder:
    def __init__(self):
        self.db = SessionLocal()
        self.faker = Faker('es_ES')
        self.batch_size = 200  # Lotes más pequeños para mayor estabilidad
    
    def run(self, total_records=10000):
        try:
            # Distribución optimizada para 10k registros
            num_users = 1500  # 15%
            num_products = 1500 # 15%
            num_comments = 3000 # 30%
            num_interactions = 4000 # 40%

            # 1. Crear usuarios con status correcto
            print(f"🔹 Creando {num_users} usuarios...")
            for i in range(0, num_users, self.batch_size):
                batch = []
                for _ in range(min(self.batch_size, num_users - i)):
                    gender = random.choice(["male", "female"])
                    first_name = self.faker.first_name_male() if gender == "male" else self.faker.first_name_female()
                    
                    batch.append(User(
                        username=f"{first_name.lower()}{random.randint(10,99)}"[:50],
                        email=f"{first_name.lower()}.{self.faker.last_name().lower()}@example.com"[:100],
                        password=self.hash_password("123456"),
                        profile_picture=f"https://randomuser.me/api/portraits/{'men' if gender == 'male' else 'women'}/{random.randint(1,99)}.jpg"[:255],
                        status='active' if random.random() > 0.3 else 'inactive',  # Valores exactos
                        registration_date=datetime.now() - timedelta(days=random.randint(0, 365))
                    ))
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Usuarios {i+1}-{i+len(batch)} creados")

            # 2. Crear productos
            print(f"\n🔹 Creando {num_products} productos...")
            categorias = ["Alimentos", "Cosméticos", "Limpieza", "Moda", "Hogar"]
            for i in range(0, num_products, self.batch_size):
                batch = []
                for _ in range(min(self.batch_size, num_products - i)):
                    batch.append(Product(
                        name=f"{random.choice(['Eco', 'Bio', 'Verde'])} {self.faker.word().capitalize()}"[:255],
                        category=f"{random.choice(categorias)} {random.choice(['Orgánico', 'Natural', 'Sostenible'])}"[:100],
                        carbon_footprint=round(random.uniform(0.5, 30.0), 2),
                        recyclable_packaging=random.choice([True, False]),
                        local_origin=random.choice([True, False]),
                        image_url=f"https://res.cloudinary.com/demo/image/upload/eco_{random.randint(1,20)}.jpg"[:500]
                    ))
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Productos {i+1}-{i+len(batch)} creados")

            # Obtener IDs existentes (optimizado)
            print("\n🔹 Obteniendo IDs para relaciones...")
            user_ids = [id[0] for id in self.db.query(User.id).yield_per(1000)]
            product_ids = [id[0] for id in self.db.query(Product.id).yield_per(1000)]

            # 3. Crear comentarios
            print(f"\n🔹 Creando {num_comments} comentarios...")
            opiniones = [
                "Muy buen producto, lo recomiendo", 
                "No cumplió con mis expectativas",
                "Calidad excelente para el precio",
                "El envío llegó tarde pero el producto es bueno",
                "Totalmente ecológico como se describe"
            ]
            for i in range(0, num_comments, self.batch_size):
                batch = []
                for _ in range(min(self.batch_size, num_comments - i)):
                    batch.append(Comment(
                        user_id=random.choice(user_ids),
                        product_id=random.choice(product_ids),
                        content=random.choice(opiniones)[:500]
                    ))
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Comentarios {i+1}-{i+len(batch)} creados")

            # 4. Crear interacciones
            print(f"\n🔹 Creando {num_interactions} interacciones...")
            for i in range(0, num_interactions, self.batch_size):
                batch = []
                for _ in range(min(self.batch_size, num_interactions - i)):
                    batch.append(Interaccion(
                        user_id=random.choice(user_ids),
                        product_id=random.choice(product_ids),
                        interaction=random.randint(1, 3)
                    ))
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Interacciones {i+1}-{i+len(batch)} creadas")

            print(f"\n🎉 Seeder completado exitosamente!")
            print(f"Total registros creados: {num_users + num_products + num_comments + num_interactions}")

        except Exception as e:
            self.db.rollback()
            print(f"\n❌ Error crítico: {str(e)}")
            raise
        finally:
            self.db.close()
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
