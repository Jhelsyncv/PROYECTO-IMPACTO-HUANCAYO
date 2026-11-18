from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class DonacionBase(BaseModel):
    item: str = Field(..., min_length=2, max_length=150, description="Nombre del alimento o insumo")
    cantidad_kg: float = Field(..., gt=0, description="Cantidad en Kg o Litros (debe ser mayor a 0)")
    comedor: str = Field(..., min_length=2, max_length=150, description="Nombre del comedor popular beneficiario")
    categoria: Optional[str] = Field("Otros", max_length=100, description="Categoría nutricional del insumo")
    donante: Optional[str] = Field("Anónimo", max_length=150, description="Donante o entidad solidaria")

    @field_validator("item", "comedor")
    @classmethod
    def validar_no_vacio(cls, valor: str) -> str:
        limpio = valor.strip()
        if not limpio:
            raise ValueError("El campo no puede estar vacío ni contener solo espacios en blanco")
        return limpio

class DonacionCrear(DonacionBase):
    pass

class DonacionSchema(DonacionBase):
    id: int
    fecha_registro: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
