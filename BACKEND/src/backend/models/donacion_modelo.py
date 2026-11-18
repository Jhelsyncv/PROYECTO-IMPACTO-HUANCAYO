from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from database import Base

def obtener_fecha_utc():
    return datetime.now(timezone.utc)

class DonacionDB(Base):
    __tablename__ = "donaciones"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String(150), nullable=False)
    cantidad_kg = Column(Float, nullable=False)
    comedor = Column(String(150), nullable=False)
    categoria = Column(String(100), default="Otros")
    donante = Column(String(150), default="Anónimo")
    fecha_registro = Column(DateTime, default=obtener_fecha_utc)
