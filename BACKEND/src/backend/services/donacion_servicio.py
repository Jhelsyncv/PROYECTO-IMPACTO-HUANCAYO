from sqlalchemy.orm import Session
from models.donacion_modelo import DonacionDB
from schemas.donacion import DonacionCrear
from fastapi import HTTPException, status

class DonacionServicio:
    """Capa de lógica de negocio y persistencia para donaciones."""

    def obtener_todas(self, db: Session) -> list[DonacionDB]:
        """Retorna todas las donaciones ordenadas de forma descendente por ID."""
        return db.query(DonacionDB).order_by(DonacionDB.id.desc()).all()

    def crear_donacion(self, db: Session, donacion: DonacionCrear) -> DonacionDB:
        """Persiste una nueva donación en PostgreSQL."""
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

    def actualizar_donacion(self, db: Session, donacion_id: int, datos: DonacionCrear) -> DonacionDB:
        """Actualiza un registro existente o lanza un error 404 si no existe."""
        donacion_existente = db.query(DonacionDB).filter(DonacionDB.id == donacion_id).first()
        if not donacion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Donación con ID {donacion_id} no encontrada"
            )

        donacion_existente.item = datos.item
        donacion_existente.cantidad_kg = datos.cantidad_kg
        donacion_existente.comedor = datos.comedor
        donacion_existente.categoria = datos.categoria or "Otros"
        donacion_existente.donante = datos.donante or "Anónimo"

        db.commit()
        db.refresh(donacion_existente)
        return donacion_existente

    def eliminar_donacion(self, db: Session, donacion_id: int) -> dict:
        """Elimina un registro o lanza un error 404 si no existe."""
        donacion = db.query(DonacionDB).filter(DonacionDB.id == donacion_id).first()
        if not donacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Donación con ID {donacion_id} no encontrada"
            )

        db.delete(donacion)
        db.commit()
        return {"mensaje": f"Donación con ID {donacion_id} eliminada correctamente"}
