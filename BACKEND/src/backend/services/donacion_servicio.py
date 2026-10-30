from sqlalchemy.orm import Session
from models.donacion_modelo import DonacionDB
from schemas.donacion import DonacionCrear
from fastapi import HTTPException, status

class DonacionServicio:

    def obtener_todas(self, db: Session):
        return db.query(DonacionDB).order_by(DonacionDB.id.desc()).all()

    def crear_donacion(self, db: Session, donacion: DonacionCrear):
        nueva_donacion = DonacionDB(
            item=donacion.item,
            cantidad_kg=donacion.cantidad_kg,
            comedor=donacion.comedor,
            categoria=donacion.categoria or "Otros",
            donante=donacion.donante or "Anónimo"
        )
        db.add(nueva_donacion)
        db.commit()
        db.refresh(nueva_donacion)
        return nueva_donacion

    def actualizar_donacion(self, db: Session, donacion_id: int, datos: DonacionCrear):
        donacion_existente = db.query(DonacionDB).filter(DonacionDB.id == donacion_id).first()
        if not donacion_existente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donación no encontrada")
        
        donacion_existente.item = datos.item
        donacion_existente.cantidad_kg = datos.cantidad_kg
        donacion_existente.comedor = datos.comedor
        donacion_existente.categoria = datos.categoria or "Otros"
        donacion_existente.donante = datos.donante or "Anónimo"
        
        db.commit()
        db.refresh(donacion_existente)
        return donacion_existente

    def eliminar_donacion(self, db: Session, donacion_id: int):
        donacion = db.query(DonacionDB).filter(DonacionDB.id == donacion_id).first()
        if not donacion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donación no encontrada")
        
        db.delete(donacion)
        db.commit()
        return {"mensaje": "Donación eliminada correctamente"}