from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ComedorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, description="Nombre del comedor popular")
    distrito: Optional[str] = Field("Huancayo", max_length=100, description="Distrito o localidad")
    direccion: Optional[str] = Field("Sector Central", max_length=200, description="Dirección física")
    responsable: Optional[str] = Field("Coordinador", max_length=100, description="Persona a cargo")
    telefono: Optional[str] = Field("964000000", max_length=50, description="Teléfono de contacto")
    es_activo: Optional[bool] = True

class ComedorCrear(ComedorBase):
    pass

class ComedorSchema(ComedorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
