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
            {"username": "Elena Díaz", "email": "elena.diaz@example.com"},
            {"username": "Valeria Torres", "email": "valeria.torres@example.com"},
            {"username": "Andrés Ramírez", "email": "andres.ramirez@example.com"},
            {"username": "Camila Mendoza", "email": "camila.mendoza@example.com"},
            {"username": "Ricardo Fernández", "email": "ricardo.fernandez@example.com"},
            {"username": "Fernanda Ruiz", "email": "fernanda.ruiz@example.com"},
            {"username": "Diego Ortega", "email": "diego.ortega@example.com"},
            {"username": "Julieta Vega", "email": "julieta.vega@example.com"},
            {"username": "Esteban Salazar", "email": "esteban.salazar@example.com"},
            {"username": "Natalia Campos", "email": "natalia.campos@example.com"},
            {"username": "Tomás Ibáñez", "email": "tomas.ibanez@example.com"},
            {"username": "Laura Silva", "email": "laura.silva@example.com"},
            {"username": "Emilio Vargas", "email": "emilio.vargas@example.com"},
            {"username": "Daniela Ríos", "email": "daniela.rios@example.com"},
            {"username": "Gustavo Molina", "email": "gustavo.molina@example.com"},
            {"username": "Patricia León", "email": "patricia.leon@example.com"},
            {"username": "Roberto Cruz", "email": "roberto.cruz@example.com"},
            {"username": "Claudia Navarro", "email": "claudia.navarro@example.com"},
            {"username": "Mauricio Herrera", "email": "mauricio.herrera@example.com"},
            {"username": "Paola Cordero", "email": "paola.cordero@example.com"},
            {"username": "Alonso Méndez", "email": "alonso.mendez@example.com"},
            {"username": "Isabela Romero", "email": "isabela.romero@example.com"},
            {"username": "Joaquín Guzmán", "email": "joaquin.guzman@example.com"},
            {"username": "Renata Vargas", "email": "renata.vargas@example.com"},
            {"username": "Fabián Soto", "email": "fabian.soto@example.com"},
            {"username": "Gabriela Pineda", "email": "gabriela.pineda@example.com"},
            {"username": "Cristian Rivas", "email": "cristian.rivas@example.com"},
            {"username": "Marina Aguilar", "email": "marina.aguilar@example.com"},
            {"username": "Iván Robles", "email": "ivan.robles@example.com"},
            {"username": "Lucía Delgado", "email": "lucia.delgado@example.com"},
            {"username": "Bruno Castillo", "email": "bruno.castillo@example.com"},
            {"username": "Silvia Torres", "email": "silvia.torres@example.com"},
            {"username": "Tomás Nieto", "email": "tomas.nieto@example.com"},
            {"username": "Valentina Peña", "email": "valentina.pena@example.com"},
            {"username": "Sebastián Arias", "email": "sebastian.arias@example.com"},
            {"username": "Manuela Cárdenas", "email": "manuela.cardenas@example.com"},
            {"username": "Ramiro Barrios", "email": "ramiro.barrios@example.com"},
            {"username": "Estela Figueroa", "email": "estela.figueroa@example.com"},
            {"username": "Franco Beltrán", "email": "franco.beltran@example.com"},
            {"username": "Marta Ibáñez", "email": "marta.ibanez@example.com"},
            {"username": "Elías Cáceres", "email": "elias.caceres@example.com"},
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
            {"name": "Champu Sólido", "category": "Limpieza"},
            {"name": "Cepillo de dientes de bambú", "category": "Hogar"},
            {"name": "Detergente biodegradable", "category": "Limpieza"},
            {"name": "Papel reciclado A4", "category": "Papeleria"},
            {"name": "Rasuradora reutilizable de acero", "category": "Hogar"},
            {"name": "Set de cubiertos de bambú", "category": "Hogar"},
            {"name": "Mochila de cáñamo", "category": "Ropa"},
            {"name": "Envoltorios de cera de abeja", "category": "Hogar"},
            {"name": "Foco LED de bajo consumo", "category": "Tecnologia"},
            {"name": "Bolsas compostables", "category": "Hogar"},
            {"name": "Desodorante natural sin aluminio", "category": "Limpieza"},
            {"name": "Toalla reutilizable de microfibra", "category": "Hogar"},
            {"name": "Jabón artesanal de avena", "category": "Limpieza"},
            {"name": "Cuaderno de papel piedra", "category": "Papeleria"},
            {"name": "Compostera de balcón", "category": "Hogar"},
            {"name": "Kit de siembra urbana", "category": "Tecnologia"},
            {"name": "Bolso de algodón reciclado", "category": "Ropa"},
            {"name": "Cepillo lavavajillas de madera", "category": "Hogar"},
            {"name": "Cera para muebles natural", "category": "Limpieza"},
            {"name": "Lámpara solar portátil", "category": "Tecnologia"},
            {"name": "Aceite esencial ecológico", "category": "Limpieza"},
            {"name": "Vasos de fibra de trigo", "category": "Hogar"},
            {"name": "Filtros de agua reutilizables", "category": "Tecnologia"},
            {"name": "Ensaladera de bambú", "category": "Hogar"},
            {"name": "Bolsa de compras plegable", "category": "Hogar"},
            {"name": "Sandalias veganas", "category": "Ropa"},
            {"name": "Camiseta tintes naturales", "category": "Ropa"},
            {"name": "Paños de limpieza compostables", "category": "Limpieza"},
            {"name": "Cargador solar", "category": "Tecnologia"},
            {"name": "Porta alimentos de acero inoxidable", "category": "Hogar"},
            {"name": "Desinfectante vegetal", "category": "Limpieza"},
            {"name": "Filtro de aire natural", "category": "Tecnologia"},
            {"name": "Kit de afeitado ecológico", "category": "Hogar"},
            {"name": "Mascarilla facial orgánica", "category": "Limpieza"},
            {"name": "Plumas biodegradables", "category": "Papeleria"},
            {"name": "Cubrebocas de tela", "category": "Ropa"},
            {"name": "Toallitas desmaquillantes reutilizables", "category": "Limpieza"},
            {"name": "Sábanas de algodón orgánico", "category": "Hogar"},
            {"name": "Bicicleta plegable ecológica", "category": "Tecnologia"},
            {"name": "Jabonera de corcho", "category": "Hogar"},
            {"name": "Limpia pisos sin químicos", "category": "Limpieza"}
        ]
        
        self.image_urls = [
            "https://images.unsplash.com/photo-1590080876434-bd4a8d8e071b",
            "https://images.unsplash.com/photo-1600185365522-5e0f9fa2badd",
            "https://images.unsplash.com/photo-1542831371-d531d36971e6",
            "https://images.unsplash.com/photo-1611095564981-0d4bfe9d1804",
            "https://images.unsplash.com/photo-1590080876434-bd4a8d8e071b",
            "https://images.unsplash.com/photo-1600185365522-5e0f9fa2badd",
            "https://images.unsplash.com/photo-1542831371-d531d36971e6",
            "https://images.unsplash.com/photo-1611095564981-0d4bfe9d1804",
            "https://images.unsplash.com/photo-1590080876434-bd4a8d8e071b",
            "https://images.unsplash.com/photo-1542831371-d531d36971e6",
            "https://images.unsplash.com/photo-1600185365522-5e0f9fa2badd",
            "https://images.unsplash.com/photo-1611095564981-0d4bfe9d1804",
            "https://images.unsplash.com/photo-1600185365522-5e0f9fa2badd",
            "https://images.unsplash.com/photo-1590080876434-bd4a8d8e071b",
            "https://images.unsplash.com/photo-1586864388020-d962b377048c",
            "https://images.unsplash.com/photo-1600661531340-6b4f44ac0b3c",
            "https://images.unsplash.com/photo-1599940824395-3227c89d67f8",
            "https://images.unsplash.com/photo-1605106702841-50fc4fbf4cbe",
            "https://images.unsplash.com/photo-1601044799967-b82fa4c62d1b",
            "https://images.unsplash.com/photo-1606760227096-204d656f5d38",
            "https://images.unsplash.com/photo-1596496052390-602a6e6e0d82",
            "https://images.unsplash.com/photo-1616627982410-33f6a9fa55fd",
            "https://images.unsplash.com/photo-1585386959984-a4155227c3d4",
            "https://images.unsplash.com/photo-1595526114035-6ca3e957f017",
            "https://images.unsplash.com/photo-1606223282975-96999e48731e",
            "https://images.unsplash.com/photo-1590080876434-bd4a8d8e071b",
            "https://images.unsplash.com/photo-1592847223854-0f474d0b8f4a",
            "https://images.unsplash.com/photo-1597451024449-184e4ae2f192",
            "https://images.unsplash.com/photo-1599076487981-bfa1eede38d8",
            "https://images.unsplash.com/photo-1579032517090-0b475948c24f",
            "https://images.unsplash.com/photo-1583337130417-3346a1b6b3c3",
            "https://images.unsplash.com/photo-1622458412352-c39b1c1730e7",
            "https://images.unsplash.com/photo-1616627982570-2dc2bcdd5f10",
            "https://images.unsplash.com/photo-1621954528935-57994a70f1a2",
            "https://images.unsplash.com/photo-1622126518176-7f5b9c8f303a",
            "https://images.unsplash.com/photo-1621629503982-68164be0c6e9",
            "https://images.unsplash.com/photo-1621788986609-9c65d94a6db5",
            "https://images.unsplash.com/photo-1583337130476-e4a38dbf12fd",
            "https://images.unsplash.com/photo-1585070598472-4360275293f7",
            "https://images.unsplash.com/photo-1592147848799-80f84b0dd3f5",
            "https://images.unsplash.com/photo-1586500056182-58e0f64f2b25",
            "https://images.unsplash.com/photo-1589987602744-0fffe177b02d",
            "https://images.unsplash.com/photo-1592422550353-5b8e6b2c9e30",
            "https://images.unsplash.com/photo-1600185365522-5e0f9fa2badd"
            
        ]

        self.profile_pictures = [
            "https://randomuser.me/api/portraits/men/32.jpg",
            "https://randomuser.me/api/portraits/women/45.jpg",
            "https://randomuser.me/api/portraits/men/76.jpg",
            "https://randomuser.me/api/portraits/women/12.jpg",
            "https://randomuser.me/api/portraits/women/68.jpg",   # Valeria Torres
            "https://randomuser.me/api/portraits/men/43.jpg",     # Andrés Ramírez
            "https://randomuser.me/api/portraits/women/28.jpg",   # Camila Mendoza
            "https://randomuser.me/api/portraits/men/81.jpg",     # Ricardo Fernández
            "https://randomuser.me/api/portraits/women/90.jpg",   # Fernanda Ruiz
            "https://randomuser.me/api/portraits/men/64.jpg",     # Diego Ortega
            "https://randomuser.me/api/portraits/women/35.jpg",   # Julieta Vega
            "https://randomuser.me/api/portraits/men/58.jpg",     # Esteban Salazar
            "https://randomuser.me/api/portraits/women/17.jpg",   # Natalia Campos
            "https://randomuser.me/api/portraits/men/25.jpg",      # Tomás Ibáñez
            "https://randomuser.me/api/portraits/women/61.jpg",
            "https://randomuser.me/api/portraits/men/34.jpg",
            "https://randomuser.me/api/portraits/women/26.jpg",
            "https://randomuser.me/api/portraits/men/50.jpg",
            "https://randomuser.me/api/portraits/women/31.jpg",
            "https://randomuser.me/api/portraits/men/17.jpg",
            "https://randomuser.me/api/portraits/women/59.jpg",
            "https://randomuser.me/api/portraits/men/46.jpg",
            "https://randomuser.me/api/portraits/women/84.jpg",
            "https://randomuser.me/api/portraits/men/10.jpg",
            "https://randomuser.me/api/portraits/women/44.jpg",
            "https://randomuser.me/api/portraits/men/73.jpg",
            "https://randomuser.me/api/portraits/women/39.jpg",
            "https://randomuser.me/api/portraits/men/67.jpg",
            "https://randomuser.me/api/portraits/women/95.jpg",
            "https://randomuser.me/api/portraits/men/20.jpg",
            "https://randomuser.me/api/portraits/women/24.jpg",
            "https://randomuser.me/api/portraits/men/91.jpg",
            "https://randomuser.me/api/portraits/women/18.jpg",
            "https://randomuser.me/api/portraits/men/15.jpg",
            "https://randomuser.me/api/portraits/women/79.jpg",
            "https://randomuser.me/api/portraits/men/13.jpg",
            "https://randomuser.me/api/portraits/women/11.jpg",
            "https://randomuser.me/api/portraits/men/48.jpg",
            "https://randomuser.me/api/portraits/women/36.jpg",
            "https://randomuser.me/api/portraits/men/60.jpg",
            "https://randomuser.me/api/portraits/women/19.jpg",
            "https://randomuser.me/api/portraits/men/70.jpg",
            "https://randomuser.me/api/portraits/women/55.jpg",
            "https://randomuser.me/api/portraits/men/29.jpg"
        ]
        
        self.sample_comments = [
            "Excelente producto, muy recomendable.",
            "Me encantó, volvería a comprarlo.",
            "Buena relación calidad-precio.",
            "No era lo que esperaba, pero funciona.",
            "Empaque ecológico, muy bien.",
            "Lo recibí a tiempo y en buen estado.",
            "Podría mejorar, pero cumple su función.",
            "Estoy satisfecho con la compra.",
            "Muy útil para reducir mi consumo de plástico.",
            "El empaque es completamente reciclable, me encanta.",
            "Buena iniciativa, excelente para el planeta.",
            "Materiales de muy buena calidad y ecológicos.",
            "Me gusta apoyar marcas conscientes.",
            "Funciona igual que uno convencional pero sin dañar el ambiente.",
            "Ideal para regalar a alguien que se preocupa por el medio ambiente.",
            "Producto natural, sin químicos innecesarios.",
            "Muy buena opción para quienes buscan alternativas sustentables.",
            "Recomiendo 100%, vale la pena cambiar a esto.",
            "Perfecto para quienes buscan alternativas sostenibles.",
            "El producto llegó en empaques reciclables, muy bien.",
            "Increíble lo cómodo y ecológico que es.",
            "Cumple su función sin generar residuos.",
            "Una excelente forma de aportar al medio ambiente.",
            "Ya es parte de mi día a día, muy útil.",
            "Lo volvería a comprar sin dudarlo.",
            "Es suave, duradero y sobre todo ecológico.",
            "Me ayudó a reducir mi basura en casa.",
            "Ideal para hogares sostenibles.",
            "Ayuda a reducir la huella de carbono.",
            "Fácil de usar y muy eficiente.",
            "Recomendado para familias que reciclan.",
            "Un producto responsable con el planeta.",
            "Me encanta su diseño natural.",
            "No pensé que funcionara tan bien siendo ecológico.",
            "Definitivamente voy a seguir comprando esta marca.",
            "Aporta a mi estilo de vida consciente.",
            "Funciona mejor que muchos productos industriales.",
            "Me sorprendió la calidad y su impacto positivo.",
            "Mis hijos también lo usan, es muy seguro.",
            "Una gran inversión para el futuro.",
            "Se siente bien saber que consumo responsablemente.",
            "Sustituí el producto anterior por este y no me arrepiento.",
            "Lo uso todos los días y no se desgasta.",
            "Gran relación calidad-precio y eco-friendly.",
            "La textura natural es increíble.",
            "Mis amigos también lo compraron tras probarlo.",
            "Huele delicioso y es 100% natural.",
            "Nunca había encontrado algo tan ecológico y útil."
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
            products_to_comment = random.sample(products, k=min(len(products), 49))  # 8 productos con comentarios
            
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
