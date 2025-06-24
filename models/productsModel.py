from sqlalchemy import Column, Integer, String, Float, Boolean
from config.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)           # Agregada longitud
    category = Column(String(100))                   # Agregada longitud
    carbon_footprint = Column(Float)
    recyclable_packaging = Column(Boolean)
    local_origin = Column(Boolean)
