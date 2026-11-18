from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from database import get_db
from schemas.donacion import DonacionCrear, DonacionSchema
from services.donacion_servicio import DonacionServicio
from services.auth_servicio import obtener_usuario_actual

router = APIRouter(prefix="/donaciones", tags=["Donaciones"])
servicio = DonacionServicio()

@router.get("", response_model=list[DonacionSchema], summary="Listar todas las donaciones")
def obtener_todas(db: Session = Depends(get_db)):
    """Obtiene el listado completo de donaciones registradas (acceso público para visualización)."""
    return servicio.obtener_todas(db)

@router.post("", response_model=DonacionSchema, status_code=status.HTTP_201_CREATED, summary="Registrar donación")
def crear(
    donacion: DonacionCrear,
    db: Session = Depends(get_db),
    usuario: str = Depends(obtener_usuario_actual)
):
    """Registra una nueva donación de insumos alimenticios. Requiere autenticación JWT."""
    return servicio.crear_donacion(db, donacion)

@router.put("/{donacion_id}", response_model=DonacionSchema, summary="Actualizar donación")
def actualizar(
    donacion_id: int = Path(..., ge=1, description="ID de la donación a modificar"),
    datos: DonacionCrear = ...,
    db: Session = Depends(get_db),
    usuario: str = Depends(obtener_usuario_actual)
):
    """Actualiza los datos de una donación existente. Requiere autenticación JWT."""
    return servicio.actualizar_donacion(db, donacion_id, datos)

@router.delete("/{donacion_id}", summary="Eliminar donación")
def eliminar(
    donacion_id: int = Path(..., ge=1, description="ID de la donación a eliminar"),
    db: Session = Depends(get_db),
    usuario: str = Depends(obtener_usuario_actual)
):
    """Elimina permanentemente una donación. Requiere autenticación JWT."""
    return servicio.eliminar_donacion(db, donacion_id)
