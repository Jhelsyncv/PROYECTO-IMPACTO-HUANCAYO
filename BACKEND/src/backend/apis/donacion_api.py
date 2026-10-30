from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.donacion import DonacionCrear, DonacionSchema
from services.donacion_servicio import DonacionServicio
from services.auth_servicio import obtener_usuario_actual  # <--- IMPORTANTE

router = APIRouter(prefix="/donaciones", tags=["Donaciones"])
servicio = DonacionServicio()

# CUALQUIERA PUEDE VER LA LISTA (SIN PROTECCIÓN)
@router.get("", response_model=list[DonacionSchema])
def obtener_todas(db: Session = Depends(get_db)):
    return servicio.obtener_todas(db)

# SOLO USUARIOS LOGUEADOS PUEDEN CREAR
@router.post("", response_model=DonacionSchema, status_code=status.HTTP_201_CREATED)
def crear(
    donacion: DonacionCrear, 
    db: Session = Depends(get_db), 
    usuario: str = Depends(obtener_usuario_actual) # <--- PROTEGIDO
):
    return servicio.crear_donacion(db, donacion)

# SOLO USUARIOS LOGUEADOS PUEDEN EDITAR
@router.put("/{donacion_id}", response_model=DonacionSchema)
def actualizar(
    donacion_id: int, 
    datos: DonacionCrear, 
    db: Session = Depends(get_db), 
    usuario: str = Depends(obtener_usuario_actual) # <--- PROTEGIDO
):
    return servicio.actualizar_donacion(db, donacion_id, datos)

# SOLO USUARIOS LOGUEADOS PUEDEN ELIMINAR
@router.delete("/{donacion_id}")
def eliminar(
    donacion_id: int, 
    db: Session = Depends(get_db), 
    usuario: str = Depends(obtener_usuario_actual) # <--- PROTEGIDO
):
    return servicio.eliminar_donacion(db, donacion_id)