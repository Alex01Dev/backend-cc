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
        self.batch_size = 200  # Lotes pequeños para estabilidad

        # Diccionario de productos ecológicos
        self.PRODUCTOS_POR_CATEGORIA = {
            "Alimentos": {
                "productos": [
                    "Pan integral", "Leche de almendras", "Miel pura", "Chocolate negro",
                    "Café", "Galletas de avena", "Aceite de oliva", "Quinoa",
                    "Pasta de trigo duro"
                ],
                "materiales": ["orgánico", "vegano", "artesanal"],
                "carbon_footprint_range": (0.5, 5.0),
                "sufijos": ["(Pack familiar)", "(Sin aditivos)", "(Energético)"]
            },
            "Ropa": {
                "productos": [
                    "Camiseta básica", "Pantalón", "Vestido largo", "Chaqueta",
                    "Calcetines", "Bragas térmicas", "Jersey", "Sombrero"
                ],
                "materiales": ["algodón orgánico", "bambú", "lino reciclado", "Piel"],
                "carbon_footprint_range": (5.0, 25.0),
                "sufijos": ["(Edición limitada)", "(Talla ética)", "(Pack 3 u.)"]
            },
            "Limpieza": {
                "productos": [
                    "Jabón", "Detergente en pastilla", "Limpiador multiusos", "Suavizante",
                    "Desinfectante natural", "Esponja vegetal", "Cepillo de madera", "Bolsa de lavado"
                ],
                "materiales": ["biodegradable", "orgánico", "Sin quimicos"],
                "carbon_footprint_range": (1.0, 8.0),
                "sufijos": ["(Zero waste)", "(Sin fragancia)", "(Concentrado)"]
            },
            "Tecnologia": {
                "productos": [
                    "Cargador solar", "Auriculares inalámbricos", "Power bank", "Fundas para móvil",
                    "Tablet", "Teclado ergonómico", "Ratón de bambú", "Altavoz portátil"
                ],
                "materiales": ["energía solar", "plástico reciclado", "metales reciclados"],
                "carbon_footprint_range": (10.0, 50.0),
                "sufijos": ["(Eficiencia A+)", "(Reparable)", "(Modular)"]
            },
            "Hogar": {
                "productos": [
                    "Vela aromática", "Taza",
                    "Tabla de cortar", "repiza"
                ],
                "materiales": ["cera", "plastico reciclado", ],
                "carbon_footprint_range": (3.0, 20.0),
                "sufijos": ["(Hecho a mano)", "(Diseño circular)"]
            },
            "Salud": {
                "productos": [
                    "Crema facial", "Protector solar", "Aceite para masaje", "Jabón íntimo",
                    "Suplemento vitamínico", "Desodorante ", "Cepillo de dientes", "Hilo dental"
                ],
                "materiales": ["a base de ingredientes naturales", "sin quimicos", "orgánico"],
                "carbon_footprint_range": (2.0, 12.0),
                "sufijos": ["(Dermatológico)", "(Sin fragancia)"]
            },
            "Papeleria": {
                "productos": [
                    "Cuaderno anillado", "Bolígrafo recargable", "Carpeta archivador", "Sobre kraft",
                    "Postales ilustradas", "Bloc de notas", "Agenda anual", "Lápices de colores"
                ],
                "materiales": ["papel semilla", "cartón reciclado", "tinta vegetal"],
                "carbon_footprint_range": (1.5, 6.0),
                "sufijos": ["(Plantable)", "(100% reciclado)"]
            },
            "Otro": {
                "productos": [
                    "Kit de jardinería", "Juego de cubiertos", "Decoración mural", "Caja regalo",
                    "Bolsa de tela", "Velas decorativas", "Portalápices", "Reloj de pared"
                ],
                "materiales": ["upcycled", "hecho a mano", "materiales mixtos"],
                "carbon_footprint_range": (2.0, 15.0),
                "sufijos": ["(Multiusos)", "(Personalizable)"]
            }
        }

    def generar_producto_ecologico(self):
        categoria = random.choice(list(self.PRODUCTOS_POR_CATEGORIA.keys()))
        datos = self.PRODUCTOS_POR_CATEGORIA[categoria]
        nombre = f"{random.choice(datos['productos'])} de {random.choice(datos['materiales'])} {random.choice(datos['sufijos'])}"
        carbon_footprint = round(random.uniform(*datos['carbon_footprint_range']), 2)

        return Product(
            name=nombre[:255],
            category=categoria[:100],
            carbon_footprint=carbon_footprint,
            recyclable_packaging=random.random() > 0.3,  # 70% True
            local_origin=random.random() > 0.6,         # 40% True
            image_url=f"https://res.cloudinary.com/ecoapp/image/{categoria.lower()}/{random.randint(1,50)}.jpg"[:500]
        )

    def run(self, total_records=10000):
        try:
            num_users = 1500   # 15%
            num_products = 1500 # 15%
            num_comments = 3000 # 30%
            num_interactions = 4000 # 40%

            # 1. Usuarios
            print(f"🔹 Creando {num_users} usuarios...")
            for i in range(0, num_users, self.batch_size):
                batch = []
                for _ in range(min(self.batch_size, num_users - i)):
                    gender = random.choice(["male", "female"])
                    first_name = self.faker.first_name_male() if gender == "male" else self.faker.first_name_female()

                    batch.append(User(
                        username=f"{first_name.lower()}{random.randint(10,99)}"[:50],
                        email=f"{first_name.lower()}.{self.faker.last_name().lower()}@gmail.com"[:100],
                        password=self.hash_password("123456"),
                        profile_picture=f"https://randomuser.me/api/portraits/{'men' if gender == 'male' else 'women'}/{random.randint(1,99)}.jpg"[:255],
                        status='active' if random.random() > 0.3 else 'inactive',
                        registration_date=datetime.now() - timedelta(days=random.randint(0, 365))
                    ))
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Usuarios {i+1}-{i+len(batch)} creados")

            # 2. Productos
            print(f"\n🔹 Creando {num_products} productos...")
            for i in range(0, num_products, self.batch_size):
                batch = [self.generar_producto_ecologico() for _ in range(min(self.batch_size, num_products - i))]
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Productos {i+1}-{i+len(batch)} creados")

            # Obtener IDs existentes
            print("\n🔹 Obteniendo IDs para relaciones...")
            user_ids = [id[0] for id in self.db.query(User.id).yield_per(1000)]
            product_ids = [id[0] for id in self.db.query(Product.id).yield_per(1000)]

            # 3. Comentarios
            print(f"\n🔹 Creando {num_comments} comentarios...")
            opiniones = [
                "Muy buen producto, lo recomiendo", 
                "No cumplió con mis expectativas",
                "Calidad excelente para el precio",
                "El envío llegó tarde pero el producto es bueno",
                "Totalmente ecológico como se describe"
            ]
            for i in range(0, num_comments, self.batch_size):
                batch = [
                    Comment(
                        user_id=random.choice(user_ids),
                        product_id=random.choice(product_ids),
                        content=random.choice(opiniones)[:500]
                    )
                    for _ in range(min(self.batch_size, num_comments - i))
                ]
                self.db.bulk_save_objects(batch)
                self.db.commit()
                print(f"✅ Comentarios {i+1}-{i+len(batch)} creados")

            # 4. Interacciones
            print(f"\n🔹 Creando {num_interactions} interacciones...")
            for i in range(0, num_interactions, self.batch_size):
                batch = [
                    Interaccion(
                        user_id=random.choice(user_ids),
                        product_id=random.choice(product_ids),
                        interaction=random.randint(1, 3)
                    )
                    for _ in range(min(self.batch_size, num_interactions - i))
                ]
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

