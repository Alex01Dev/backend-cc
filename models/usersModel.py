from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class Usuario(Base):
    __tablename__ = "tbb_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID único del usuario')
    nombre_usuario = Column(String(60), nullable=False, comment='Nombre del usuario')
    correo_electronico = Column(String(100), nullable=False, comment='Correo electrónico del usuario')
    contrasena = Column(String(128), nullable=False, comment='Contraseña cifrada del usuario')
    estatus = Column(Enum('Activo', 'Inactivo'), nullable=False, comment='Estado actual del usuario')
    fecha_registro = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=True)