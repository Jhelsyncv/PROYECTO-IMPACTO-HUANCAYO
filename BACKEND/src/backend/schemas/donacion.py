from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from datetime import datetime
from typing import Optional, Any

class DonacionBase(BaseModel):
    item: str = Field(..., min_length=2, max_length=150, description="Nombre del alimento o insumo")
    cantidad_kg: float = Field(..., gt=0, description="Cantidad en Kg o Litros (debe ser mayor a 0)")
    comedor: Optional[str] = Field(None, description="Nombre descriptivo del comedor popular")
    categoria: Optional[str] = Field("Otros", max_length=100, description="Categoría nutricional del insumo")
    comedor_id: Optional[int] = Field(None, description="ID del comedor popular (Normalización 3FN)")
    categoria_id: Optional[int] = Field(None, description="ID de la categoría (Normalización 3FN)")
    donante: Optional[str] = Field("Anónimo", max_length=150, description="Donante o entidad solidaria")

    @field_validator("item")
    @classmethod
    def validar_no_vacio(cls, valor: str) -> str:
        limpio = valor.strip()
        if not limpio:
            raise ValueError("El nombre del alimento no puede estar vacío")
        return limpio

class DonacionCrear(DonacionBase):
    pass

class DonacionSchema(DonacionBase):
    id: int
    fecha_registro: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="wrap")
    @classmethod
    def resolver_relaciones(cls, val: Any, handler):
        """Resuelve dinámicamente los nombres de comedor y categoría desde las relaciones 3FN."""
        if hasattr(val, "comedor_rel") or hasattr(val, "categoria_rel"):
            comedor_rel = getattr(val, "comedor_rel", None)
            categoria_rel = getattr(val, "categoria_rel", None)

            comedor_nombre = comedor_rel.nombre if comedor_rel else getattr(val, "comedor", "Sin Comedor")
            categoria_nombre = categoria_rel.nombre if categoria_rel else getattr(val, "categoria", "Otros")

            data = {
                "id": getattr(val, "id", None),
                "item": getattr(val, "item", ""),
                "cantidad_kg": getattr(val, "cantidad_kg", 0.0),
                "comedor": comedor_nombre or "Comedor Popular",
                "categoria": categoria_nombre or "Otros",
                "comedor_id": getattr(val, "comedor_id", None),
                "categoria_id": getattr(val, "categoria_id", None),
                "donante": getattr(val, "donante", "Anónimo") or "Anónimo",
                "fecha_registro": getattr(val, "fecha_registro", None)
            }
            return handler(data)
        return handler(val)
