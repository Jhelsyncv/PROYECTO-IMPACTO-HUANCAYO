from fastapi import APIRouter
from schemas.donacion import Donacion, DonacionCrear
from services.donacion_servicio import donacion_servicio

router = APIRouter(prefix="/donaciones", tags=["Donaciones"])

@router.get("/", response_model=list[Donacion])
def listar_donaciones():
    return donacion_servicio.obtener_todas()

@router.post("/", response_model=Donacion)
def guardar_donacion(donacion: DonacionCrear):
    return donacion_servicio.crear_donacion(donacion)