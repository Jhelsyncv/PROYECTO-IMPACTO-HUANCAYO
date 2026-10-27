from sqlalchemy import Column, Integer, String, Float
from database import Base

class DonacionDB(Base):
    __tablename__ = "donaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String, nullable=False)
    cantidad_kg = Column(Float, nullable=False)
    comedor = Column(String, nullable=False)