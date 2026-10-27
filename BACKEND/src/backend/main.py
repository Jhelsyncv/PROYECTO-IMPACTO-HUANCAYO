from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from apis.donacion_api import router as donacion_router

# Crea la tabla en PostgreSQL si no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Donaciones Comedores Huancayo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(donacion_router)