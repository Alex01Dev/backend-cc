from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
import os

# Obtener DATABASE_URL de las variables de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')

# Si no hay DATABASE_URL en entorno (desarrollo local), usar la local
if not DATABASE_URL:
    DATABASE_URL = "mysql+pymysql://root:12345@localhost:3306/db_cc"
else:
    # Si DATABASE_URL empieza con mysql://, cambiar a mysql+pymysql://
    if DATABASE_URL.startswith('mysql://'):
        DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://', 1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()