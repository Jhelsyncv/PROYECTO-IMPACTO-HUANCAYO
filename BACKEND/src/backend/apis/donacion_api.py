from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.donacion import DonacionSchema, DonacionCrear
from services.donacion_servicio import DonacionServicio
from typing import List

router = APIRouter(prefix="/donaciones", tags=["Donaciones"])
servicio = DonacionServicio()

@router.get("", response_model=List[DonacionSchema])
def listar_donaciones(db: Session = Depends(get_db)):
    return servicio.obtener_todas(db)

@router.post("", response_model=DonacionSchema, status_code=status.HTTP_201_CREATED)
def registrar_donacion(donacion: DonacionCrear, db: Session = Depends(get_db)):
    return servicio.crear_donacion(db, donacion)

@router.put("/{donacion_id}", response_model=DonacionSchema)
def actualizar_donacion(donacion_id: int, donacion: DonacionCrear, db: Session = Depends(get_db)):
    return servicio.actualizar_donacion(db, donacion_id, donacion)

@router.delete("/{donacion_id}")
def eliminar_donacion(donacion_id: int, db: Session = Depends(get_db)):
    return servicio.eliminar_donacion(db, donacion_id)