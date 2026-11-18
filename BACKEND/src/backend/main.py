import sys

# Compatibilidad para Python 3.9 con Pydantic v2 JSON Schema / OpenAPI
if sys.version_info < (3, 10):
    try:
        import pydantic.json_schema
        _orig_get_literal_values = pydantic.json_schema.get_literal_values

        def _compat_get_literal_values(annotation, **kwargs):
            for val in _orig_get_literal_values(annotation, **kwargs):
                if hasattr(val, '__args__'):
                    yield from _compat_get_literal_values(val, **kwargs)
                else:
                    yield val

        pydantic.json_schema.get_literal_values = _compat_get_literal_values
    except Exception:
        pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from apis.donacion_api import router as donacion_router
from routers.auth_router import router as auth_router

# 1. Crear las tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)

# 2. Instanciar la aplicación FastAPI con metadatos descriptivos para OpenAPI/Swagger
app = FastAPI(
    title="API AlimentaHuancayo - Comedores Populares",
    description="API REST para el registro, seguimiento y administración de donaciones alimentarias.",
    version="1.0.0"
)

# 3. Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Endpoint raíz de verificación
@app.get("/", tags=["Salud del Sistema"])
def estado_api():
    """Endpoint raíz que confirma el estado operativo de la API."""
    return {
        "proyecto": "AlimentaHuancayo - Comedores Populares",
        "estado": "En línea y operativo",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

# 5. Incluir los Routers modulares
app.include_router(auth_router)
app.include_router(donacion_router)
