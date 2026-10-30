from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.usuario_modelo import UsuarioDB
from services.auth_servicio import verificar_password, obtener_password_hash, crear_token_acceso
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class RegistroSchema(BaseModel):
    nombre: str
    email: EmailStr
    password: str

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(datos: RegistroSchema, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioDB).filter(UsuarioDB.email == datos.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = UsuarioDB(
        nombre=datos.nombre,
        email=datos.email,
        password_hash=obtener_password_hash(datos.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    return {"mensaje": "Usuario registrado exitosamente"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == form_data.username).first()
    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    access_token = crear_token_acceso(data={"sub": usuario.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "usuario": {"nombre": usuario.nombre, "email": usuario.email}
    }