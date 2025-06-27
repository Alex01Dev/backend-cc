from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from config.db import get_db
from config.jwt import create_access_token, get_current_user

from models.usersModel import Usuario as UsuarioDB
from schemas.userSchemas import UsuarioLogin, UsuarioCreate, Usuario, UsuarioSimple

from controller.userController import (
    authenticate_user,
    get_user_by_nombre_usuario,
    get_user_by_nombre_usuario_or_email,
    get_user_by_id,
    create_user,
    get_usuarios_gerentes
)

user = APIRouter()
security = HTTPBearer()


# ✅ Login
@user.post("/login", response_model=dict, tags=["Autenticación"])
async def login(user_data: UsuarioLogin, db: Session = Depends(get_db)):
    user = authenticate_user(
        db, nombre_usuario=user_data.nombre_usuario, contrasena=user_data.contrasena
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.nombre_usuario},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuarioLogueado": user.nombre_usuario,
        "correo_usuario": user.correo_electronico
    }


# ✅ Registro de usuario
@user.post("/register", response_model=Usuario, tags=["Usuarios"])
async def register_new_user(user_data: UsuarioCreate, db: Session = Depends(get_db)):
    user_data.estatus = user_data.estatus or "Activo"

    existing_user = get_user_by_nombre_usuario_or_email(
        db=db,
        nombre_usuario=user_data.nombre_usuario,
        correo_electronico=user_data.correo_electronico
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    return create_user(db=db, user=user_data)


# ✅ Obtener usuario por ID
@user.get("/users/{id}", response_model=Usuario, tags=["Usuarios"])
async def read_user(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_user = get_user_by_id(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


# ✅ Obtener usuario por nombre de usuario
@user.get("/usuario/{nombre_usuario}", tags=["Usuarios"])
async def get_usuario_basico(nombre_usuario: str, db: Session = Depends(get_db)):
    usuario = get_user_by_nombre_usuario(db, nombre_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "correo": usuario.correo_electronico,
        "fecha_registro": usuario.fecha_registro,
        "estatus": usuario.estatus
    }


# ✅ Obtener lista de usuarios con estatus activo (si tienes lógica de gerente, puede ajustarse)
@user.get("/usuarios", response_model=List[UsuarioSimple], tags=["Usuarios"])
def obtener_usuarios_activos(db: Session = Depends(get_db)):
    usuarios = get_usuarios_gerentes(db)  # Puedes renombrar esto si se aplica a todos los usuarios activos
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return [{"id": u.id, "nombre_usuario": u.nombre_usuario, "estatus": u.estatus} for u in usuarios]
