from sqlalchemy.orm import Session
from models.donacion_modelo import DonacionDB
from models.comedor_modelo import ComedorDB
from models.categoria_modelo import CategoriaDB
from schemas.donacion import DonacionCrear
from fastapi import HTTPException, status

class DonacionServicio:
    """Capa de lógica de negocio y persistencia normalizada (3FN) para donaciones."""

    def _resolver_comedor_id(self, db: Session, nombre_comedor: str, comedor_id: int = None) -> int:
        """Obtiene o registra el comedor popular para garantizar la normalización 3FN."""
        if comedor_id:
            existente = db.query(ComedorDB).filter(ComedorDB.id == comedor_id).first()
            if existente:
                return existente.id

        if nombre_comedor and nombre_comedor.strip():
            nombre_limpio = nombre_comedor.strip()
            comedor = db.query(ComedorDB).filter(ComedorDB.nombre.ilike(nombre_limpio)).first()
            if not comedor:
                comedor = ComedorDB(
                    nombre=nombre_limpio,
                    distrito="Huancayo",
                    direccion="Comedor Popular Registrado"
                )
                db.add(comedor)
                db.commit()
                db.refresh(comedor)
            return comedor.id
        return None

    def _resolver_categoria_id(self, db: Session, nombre_categoria: str, categoria_id: int = None) -> int:
        """Obtiene o registra la categoría para garantizar la normalización 3FN."""
        if categoria_id:
            existente = db.query(CategoriaDB).filter(CategoriaDB.id == categoria_id).first()
            if existente:
                return existente.id

        if nombre_categoria and nombre_categoria.strip():
            nombre_limpio = nombre_categoria.strip()
            cat = db.query(CategoriaDB).filter(CategoriaDB.nombre.ilike(nombre_limpio)).first()
            if not cat:
                cat = CategoriaDB(
                    nombre=nombre_limpio,
                    descripcion="Categoría alimenticia"
                )
                db.add(cat)
                db.commit()
                db.refresh(cat)
            return cat.id
        return None

    def obtener_todas(self, db: Session) -> list[DonacionDB]:
        """Retorna todas las donaciones ordenadas de forma descendente por ID."""
        return db.query(DonacionDB).order_by(DonacionDB.id.desc()).all()

    def crear_donacion(self, db: Session, donacion: DonacionCrear) -> DonacionDB:
        """Persiste una nueva donación vinculada a comedores y categorías (3FN)."""
        com_id = self._resolver_comedor_id(db, donacion.comedor, donacion.comedor_id)
        cat_id = self._resolver_categoria_id(db, donacion.categoria, donacion.categoria_id)

        nueva_donacion = DonacionDB(
            item=donacion.item.strip(),
            cantidad_kg=donacion.cantidad_kg,
            comedor_id=com_id,
            categoria_id=cat_id,
            comedor=donacion.comedor.strip() if donacion.comedor else "Comedor Popular",
            categoria=donacion.categoria or "Otros",
            donante=donacion.donante.strip() if donacion.donante else "Anónimo"
        )
        db.add(nueva_donacion)
        db.commit()
        db.refresh(nueva_donacion)
        return nueva_donacion

    def actualizar_donacion(self, db: Session, donacion_id: int, datos: DonacionCrear) -> DonacionDB:
        """Actualiza un registro existente y sincroniza sus relaciones foráneas."""
        donacion_existente = db.query(DonacionDB).filter(DonacionDB.id == donacion_id).first()
        if not donacion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Donación con ID {donacion_id} no encontrada"
            )

        com_id = self._resolver_comedor_id(db, datos.comedor, datos.comedor_id)
        cat_id = self._resolver_categoria_id(db, datos.categoria, datos.categoria_id)

        donacion_existente.item = datos.item.strip()
        donacion_existente.cantidad_kg = datos.cantidad_kg
        donacion_existente.comedor_id = com_id
        donacion_existente.categoria_id = cat_id
        donacion_existente.comedor = datos.comedor.strip() if datos.comedor else "Comedor Popular"
        donacion_existente.categoria = datos.categoria or "Otros"
        donacion_existente.donante = datos.donante.strip() if datos.donante else "Anónimo"

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
