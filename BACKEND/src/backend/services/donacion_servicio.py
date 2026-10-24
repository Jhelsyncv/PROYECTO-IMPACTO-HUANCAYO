from schemas.donacion import Donacion, DonacionCrear

class DonacionServicio:
    def __init__(self):
        self._db: list[Donacion] = []
        self._id_counter = 1

    def obtener_todas(self) -> list[Donacion]:
        return self._db

    def crear_donacion(self, datos: DonacionCrear) -> Donacion:
        nueva_donacion = Donacion(
            id=self._id_counter,
            item=datos.item,
            cantidad_kg=datos.cantidad_kg,
            comedor=datos.comedor
        )
        self._db.append(nueva_donacion)
        self._id_counter += 1
        return nueva_donacion

donacion_servicio = DonacionServicio()