from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class DonacionDB(Base):
    __tablename__ = "donaciones"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    cantidad_kg = Column(Float, nullable=False)
    comedor = Column(String, nullable=False)
    categoria = Column(String, default="Otros")
    donante = Column(String, default="Anónimo")
    fecha_registro = Column(DateTime, default=datetime.utcnow)
   