from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría")
    descripcion: Optional[str] = Field("Insumos alimenticios", max_length=255, description="Descripción del grupo de alimentos")

class CategoriaCrear(CategoriaBase):
    pass

class CategoriaSchema(CategoriaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
