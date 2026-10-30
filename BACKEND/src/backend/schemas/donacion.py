from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DonacionBase(BaseModel):
    item: str
    cantidad_kg: float
    comedor: str
    categoria: Optional[str] = "Otros"
    donante: Optional[str] = "Anónimo"

class DonacionCrear(DonacionBase):
    pass

class DonacionSchema(DonacionBase):
    id: int
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True