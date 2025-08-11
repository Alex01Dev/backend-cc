from pydantic import BaseModel
from datetime import datetime

# Subesquema para mostrar información básica del usuario
class UserSimple(BaseModel):
    id: int
    username: str
    profile_picture: str 

    class Config:
        from_attributes = True

# Esquema para crear comentarios (lo que se envía desde el frontend)
class CommentCreate(BaseModel):
    product_id: int
    content: str

# Esquema para mostrar comentarios sin incluir info del usuario
class CommentOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

# Esquema para mostrar comentarios con info del usuario
class CommentWithUser(BaseModel):
    id: int
    user_id: int
    product_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None
    user: UserSimple  # Aquí va el objeto anidado con id y username del usuario

    class Config:
        from_attributes = True
