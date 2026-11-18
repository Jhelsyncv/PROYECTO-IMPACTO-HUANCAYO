from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class CategoriaDB(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True, default="Insumos alimenticios")

    # Relación 1:N con donaciones
    donaciones = relationship("DonacionDB", back_populates="categoria_rel")
