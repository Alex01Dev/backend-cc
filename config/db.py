from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import pymysql

# Instalar pymysql como driver MySQL (importante para SSL)
pymysql.install_as_MySQLdb()

# Obtener DATABASE_URL de las variables de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')

# Si no hay DATABASE_URL en entorno (desarrollo local), usar la local
if not DATABASE_URL:
    # Desarrollo local
    DATABASE_URL = "mysql+pymysql://root:12345@localhost:3306/db_cc"
    engine = create_engine(DATABASE_URL)
else:
    # Producción (Aiven en Render)
    
    # Asegurar formato correcto
    if DATABASE_URL.startswith('mysql://'):
        DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)
    
    # Configuración específica para Aiven con SSL
    ssl_args = {
        'ssl': {
            'ca': '/etc/ssl/certs/ca-certificates.crt',
            'check_hostname': False
        }
    }
    
    # Crear engine con configuración para Aiven
    engine = create_engine(
        DATABASE_URL,
        connect_args=ssl_args,
        pool_pre_ping=True,           # Verificar conexión antes de usar
        pool_recycle=300,             # Reciclar conexiones cada 5 minutos
        pool_size=5,                  # Número de conexiones en el pool
        max_overflow=10,              # Máximo de conexiones adicionales
        echo=False                    # Cambia a True para debug
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()