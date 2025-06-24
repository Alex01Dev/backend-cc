from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    carbon_footprint: float
    recyclable_packaging: bool
    local_origin: bool

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Habilita compatibilidad con ORM
