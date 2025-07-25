from pydantic import BaseModel, HttpUrl
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
    category: CategoriaProducto
    carbon_footprint: float
    recyclable_packaging: bool
    local_origin: bool

class ProductCreate(ProductBase):
    pass  # no lleva imagen porque se sube aparte

class Product(ProductBase):
    id: int
    image_url: HttpUrl | None = None  # NUEVO

    class Config:
        from_attributes = True
