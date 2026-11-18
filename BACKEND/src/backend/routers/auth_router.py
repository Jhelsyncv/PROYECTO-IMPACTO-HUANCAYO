from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.usuario_modelo import UsuarioDB
from services.auth_servicio import (
    verificar_password,
    obtener_password_hash,
    crear_token_acceso
)
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class RegistroSchema(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña (mínimo 6 caracteres)")

class UsuarioInfoSchema(BaseModel):
    nombre: str
    email: str

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioInfoSchema

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(datos: RegistroSchema, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en la base de datos con contraseña encriptada."""
    usuario_existente = db.query(UsuarioDB).filter(UsuarioDB.email == datos.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado en el sistema"
        )

    nuevo_usuario = UsuarioDB(
        nombre=datos.nombre.strip(),
        email=datos.email.lower().strip(),
        password_hash=obtener_password_hash(datos.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {
        "mensaje": "Usuario registrado exitosamente",
        "usuario": {"id": nuevo_usuario.id, "nombre": nuevo_usuario.nombre, "email": nuevo_usuario.email}
    }

@router.post("/login", response_model=TokenResponseSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica las credenciales del usuario y genera el token JWT Bearer."""
    email_limpio = form_data.username.lower().strip()
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email_limpio).first()

    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = crear_token_acceso(data={"sub": usuario.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {"nombre": usuario.nombre, "email": usuario.email}
    }
