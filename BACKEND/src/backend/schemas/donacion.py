from pydantic import BaseModel

class DonacionBase(BaseModel):
    item: str
    cantidad_kg: float
    comedor: str

class DonacionCrear(DonacionBase):
    pass

class DonacionSchema(DonacionBase):
    id: int

    class Config:
        from_attributes = True

