from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# ============================================
# CONFIGURACIÓN BASE DE DATOS - VERSIÓN SIMPLE
# ============================================

# 1. Obtener credenciales de Render
DB_HOST = os.environ.get('DB_HOST', 'mysql-2b45c406-alex-74a3.j.aivencloud.com')
DB_USER = os.environ.get('DB_USER', 'avnadmin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'AVNS_nUGv/Me6QC6X-Ax4VNF')
DB_PORT = os.environ.get('DB_PORT', '15361')
DB_NAME = os.environ.get('DB_NAME', 'defaultdb')

print("📊 Configurando base de datos...")

# 2. Codificar la contraseña (porque tiene /)
encoded_password = quote_plus(DB_PASSWORD)

# 3. Crear URL de conexión
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL += "?ssl_ca=/etc/ssl/certs/ca-certificates.crt&ssl_mode=REQUIRED"

print(f"✅ URL creada (sin contraseña): mysql+pymysql://{DB_USER}:******@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 4. Crear motor de base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # Verifica conexión antes de usar
    pool_recycle=280,        # Recicla conexiones
    pool_size=5,             # 5 conexiones máximo
    echo=False               # Cambia a True para ver SQL
)

# 5. Configurar sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 6. Función para obtener conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()