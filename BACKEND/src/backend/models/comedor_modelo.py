from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class ComedorDB(Base):
    __tablename__ = "comedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), unique=True, nullable=False, index=True)
    distrito = Column(String(100), default="Huancayo")
    direccion = Column(String(200), default="Huancayo, Junín")
    responsable = Column(String(100), default="Coordinador de Comedor")
    telefono = Column(String(50), default="964000000")
    es_activo = Column(Boolean, default=True)

    # Relación 1:N con donaciones
    donaciones = relationship("DonacionDB", back_populates="comedor_rel")
