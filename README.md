# Sistema de Gestión de Donaciones - Comedores Populares de Huancayo

Plataforma web full-stack orientada a la administración, seguimiento estadístico y control en tiempo real de donaciones de insumos alimenticios para comedores populares en la provincia de Huancayo, Perú.

---

## Arquitectura del Sistema

* **Frontend:** Angular 17/18 (Standalone Components, SSR Guard, Bootstrap 5, Chart.js, SheetJS, jsPDF).
* **Backend:** FastAPI (Python 3.9+), SQLAlchemy ORM, Pydantic v2.
* **Base de Datos:** PostgreSQL.
* **Seguridad:** Autenticación JWT (JSON Web Tokens), Encriptación Bcrypt, Protección CORS.

---

## Estructura del Proyecto

```text
PROYECTO-IMPACTO-HUANCAYO/
│
├── BACKEND/
│   ├── src/
│   │   └── backend/
│   │       ├── apis/            # Endpoints REST (donacion_api.py)
│   │       ├── models/          # Modelos SQLAlchemy (PostgreSQL)
│   │       ├── routers/         # Rutas de Autenticación (auth_router.py)
│   │       ├── schemas/         # Validaciones Pydantic
│   │       ├── services/        # Lógica de Negocio y Auth JWT
│   │       ├── database.py      # Conexión PostgreSQL
│   │       ├── main.py          # Punto de entrada FastAPI
│   │       └── seed_admin.py    # Script de inicialización de administrador
│   └── requirements.txt
│
└── FRONTEND/
    ├── src/
    │   ├── app/
    │   │   ├── components/      # Módulo principal de donaciones
    │   │   └── services/        # Servicios HTTP Angular (Donaciones y Auth)
    │   └── index.html           # Inclusión de CDN (Chart.js, SheetJS, jsPDF)
    └── angular.json
```

---

## Instalación y Configuración

### 1. Base de Datos (PostgreSQL)
Crea la base de datos en pgAdmin o PostgreSQL CLI:
```sql
CREATE DATABASE donaciones_db;
```

### 2. Backend (FastAPI)
```bash
cd BACKEND
pip install -r requirements.txt
python src/backend/seed_admin.py   # Crea el usuario administrador por defecto
uvicorn main:app --app-dir src/backend --reload
```
* **API Documentación Interactiva (Swagger):** `http://127.0.0.1:8000/docs`

### 3. Frontend (Angular)
```bash
cd FRONTEND
npm install
ng serve
```
* **Aplicación Web:** `http://localhost:4200`

---

## Endpoints Principales de la API

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| `GET` | `/donaciones` | Listar todas las donaciones | Público |
| `POST` | `/donaciones` | Registrar una nueva donación | Recomienda JWT |
| `PUT` | `/donaciones/{id}` | Actualizar un registro existente | Recomienda JWT |
| `DELETE` | `/donaciones/{id}` | Eliminar un registro | Recomienda JWT |
| `POST` | `/auth/login` | Autenticación de usuario y obtención de token | Público |
| `POST` | `/auth/registro` | Registro de nuevos usuarios | Público |

---

## Credenciales por Defecto

* **Usuario:** `admin@comedores.pe`
* **Contraseña:** `admin123`