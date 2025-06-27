from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre_usuario: str
    correo_electronico: EmailStr
    estatus: str

class UsuarioCreate(UsuarioBase):
    contrasena: str

class Usuario(BaseModel):
    id: int
    nombre_usuario: str
    correo_electronico: EmailStr
    estatus: str
    fecha_registro: datetime
    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str

class UsuarioSimple(BaseModel):
    id: int
    nombre_usuario: str
    estatus: str
    class Config:
        orm_mode = True
