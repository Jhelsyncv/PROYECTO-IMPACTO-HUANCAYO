import sys
from pathlib import Path

# Añadir la carpeta raíz del código al path
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.donacion_api import router as donacion_router

app = FastAPI(title="API Impacto Social - Huancayo")

# Permitir solicitudes desde Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(donacion_router)

@app.get('/')
def saludo():
    return {'mensaje': 'Bienvenidos a la API de Donaciones'}