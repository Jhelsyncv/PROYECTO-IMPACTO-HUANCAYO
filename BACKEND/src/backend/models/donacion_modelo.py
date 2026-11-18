from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

def obtener_fecha_utc():
    return datetime.now(timezone.utc)

class DonacionDB(Base):
    __tablename__ = "donaciones"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String(150), nullable=False)
    cantidad_kg = Column(Float, nullable=False)
    
    # Claves foráneas (Normalización 3FN)
    comedor_id = Column(Integer, ForeignKey("comedores.id", ondelete="SET NULL"), nullable=True, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Campos de texto preservados para retrocompatibilidad
    comedor = Column(String(150), nullable=True)
    categoria = Column(String(100), default="Otros")
    donante = Column(String(150), default="Anónimo")
    fecha_registro = Column(DateTime, default=obtener_fecha_utc)

    # Relaciones SQLAlchemy ORM
    comedor_rel = relationship("ComedorDB", back_populates="donaciones", lazy="joined")
    categoria_rel = relationship("CategoriaDB", back_populates="donaciones", lazy="joined")
