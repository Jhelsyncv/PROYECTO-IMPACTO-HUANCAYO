from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from models.comedor_modelo import ComedorDB
from schemas.comedor import ComedorSchema, ComedorCrear
from services.auth_servicio import obtener_usuario_actual

router = APIRouter(prefix="/comedores", tags=["Comedores Populares (3FN)"])

@router.get("", response_model=list[ComedorSchema], summary="Listar comedores populares")
def listar_comedores(db: Session = Depends(get_db)):
    """Retorna la lista de comedores populares registrados en Huancayo."""
    return db.query(ComedorDB).order_by(ComedorDB.nombre.asc()).all()

@router.post("", response_model=ComedorSchema, status_code=status.HTTP_201_CREATED, summary="Registrar comedor popular")
def registrar_comedor(
    datos: ComedorCrear,
    db: Session = Depends(get_db),
    usuario: str = Depends(obtener_usuario_actual)
):
    """Registra un nuevo comedor popular en la base de datos (requiere autenticación JWT)."""
    comedor = ComedorDB(
        nombre=datos.nombre.strip(),
        distrito=datos.distrito or "Huancayo",
        direccion=datos.direccion or "Sector Central",
        responsable=datos.responsable or "Coordinador",
        telefono=datos.telefono or "964000000",
        es_activo=datos.es_activo if datos.es_activo is not None else True
    )
    db.add(comedor)
    db.commit()
    db.refresh(comedor)
    return comedor
