from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from apis.donacion_api import router as donacion_router
from routers.auth_router import router as auth_router

# 1. Crear las tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)

# 2. Instanciar la aplicación FastAPI
app = FastAPI(title="API Donaciones Comedores Huancayo")

# 3. Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Incluir los Routers
app.include_router(auth_router)
app.include_router(donacion_router)