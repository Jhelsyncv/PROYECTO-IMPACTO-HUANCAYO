from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.categoria_modelo import CategoriaDB
from schemas.categoria import CategoriaSchema

router = APIRouter(prefix="/categorias", tags=["Categorías de Alimentos (3FN)"])

@router.get("", response_model=list[CategoriaSchema], summary="Listar categorías nutricionales")
def listar_categorias(db: Session = Depends(get_db)):
    """Retorna las categorías de alimentos disponibles para clasificación de donaciones."""
    return db.query(CategoriaDB).order_by(CategoriaDB.nombre.asc()).all()
