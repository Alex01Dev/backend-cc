from pydantic import BaseModel
from enum import Enum

class CategoriaProducto(str, Enum):
    alimentos = "Alimentos"
    ropa = "Ropa"
    tecnologia = "Tecnologia"
    limpieza = "Limpieza"
    hogar = "Hogar"
    salud = "Salud"
    bebidas = "Bebidas"
    papeleria = "Papeleria"
    otros = "Otros"

class ProductBase(BaseModel):
    name: str
    category: CategoriaProducto  # Aquí usamos el Enum directamente
    carbon_footprint: float
    recyclable_packaging: bool
    local_origin: bool

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
