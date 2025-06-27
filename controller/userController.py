from sqlalchemy.orm import Session
from models.usersModel import Usuario
from schemas.userSchemas import UsuarioCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(db: Session, id: int):
    return db.query(Usuario).filter(Usuario.id == id).first()

def get_user_by_nombre_usuario(db: Session, nombre_usuario: str):
    return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

def get_user_by_nombre_usuario_or_email(db: Session, nombre_usuario: str, correo_electronico: str):
    return db.query(Usuario).filter(
        (Usuario.nombre_usuario == nombre_usuario) |
        (Usuario.correo_electronico == correo_electronico)
    ).first()

def create_user(db: Session, user: UsuarioCreate):
    hashed_password = pwd_context.hash(user.contrasena)
    db_user = Usuario(
        nombre_usuario=user.nombre_usuario,
        correo_electronico=user.correo_electronico,
        contrasena=hashed_password,
        estatus=user.estatus
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, nombre_usuario: str, contrasena: str):
    user = get_user_by_nombre_usuario(db, nombre_usuario)
    if not user:
        return None
    if not pwd_context.verify(contrasena, user.contrasena):
        return None
    return user

def get_usuarios_gerentes(db: Session):
    # Si ya no manejas roles, puedes devolver todos los usuarios activos
    return db.query(Usuario).filter(Usuario.estatus == "Activo").all()
