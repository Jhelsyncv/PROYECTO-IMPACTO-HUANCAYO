# Sistema de Gestión de Donaciones - Comedores Populares de Huancayo (AlimentaHuancayo)

Plataforma web orientada a la administración, seguimiento estadístico y control en tiempo real de donaciones de insumos alimenticios para comedores populares en la provincia de Huancayo, Perú.

---

## 🏛️ Arquitectura del Sistema

* **Frontend:** Angular 22 (Standalone Components, Zoneless Change Detection, SSR Guard, Bootstrap 5.3 nativo sin CSS personalizado, Chart.js, SheetJS, jsPDF).
* **Backend:** FastAPI (Python 3.9+), SQLAlchemy ORM 2.0, Pydantic v2, Dotenv.
* **Base de Datos:** PostgreSQL normalizada hasta **3FN (Tercera Forma Normal)** con claves foráneas e integridad referencial.
* **Seguridad:** Autenticación JWT (JSON Web Tokens), Encriptación Bcrypt, Protección CORS.
* **Control de Versiones:** Git con ramas temáticas (`feature/...`) y Pull Requests integrados.

---

## 📁 Estructura del Proyecto

```text
PROYECTO-IMPACTO-HUANCAYO/
│
├── BACKEND/
│   ├── src/
│   │   └── backend/
│   │       ├── apis/            # Endpoints REST (donacion_api, comedor_api, categoria_api)
│   │       ├── models/          # Modelos SQLAlchemy 3FN (Usuario, Comedor, Categoria, Donacion)
│   │       ├── routers/         # Rutas de Autenticación (auth_router.py)
│   │       ├── schemas/         # Validaciones Pydantic v2
│   │       ├── services/        # Lógica de Negocio y Auth JWT
│   │       ├── database.py      # Conexión PostgreSQL desacoplada (.env)
│   │       ├── main.py          # Punto de entrada FastAPI con OpenAPI/Swagger
│   │       ├── seed_admin.py    # Inicialización de usuario administrador
│   │       └── seed_3fn.py      # Inicialización y sembrado de datos en 3FN
│   ├── schema_3fn.sql           # Script DDL completo de base de datos normalizada
│   ├── .env.example             # Plantilla de variables de entorno
│   └── requirements.txt         # Dependencias exactas de Python
│
└── FRONTEND/
    ├── src/
    │   ├── app/
    │   │   ├── components/      # Componente principal DonacionComponente (Bootstrap 5 nativo)
    │   │   ├── interfaces/      # Interfaces TypeScript unificadas
    │   │   └── services/        # Servicios HTTP Angular (Donaciones y Auth)
    │   ├── index.html           # Inclusión de Bootstrap 5.3 e Iconos
    │   └── styles.css           # 0% CSS propio (100% Bootstrap 5 nativo)
    └── angular.json
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Base de Datos (PostgreSQL)
Crea la base de datos en pgAdmin o PostgreSQL CLI:
```sql
CREATE DATABASE donaciones_db;
```
*(Opcional: puedes ejecutar directamente el script `BACKEND/schema_3fn.sql`)*.

### 2. Backend (FastAPI)
```bash
cd BACKEND
pip install -r requirements.txt
python src/backend/seed_admin.py   # Crea el administrador por defecto
python src/backend/seed_3fn.py     # Siembra comedores, categorías y normaliza a 3FN
uvicorn main:app --app-dir src/backend --reload --port 8000
```
* **API Documentación Interactiva (Swagger UI):** `http://127.0.0.1:8000/docs`
* **Especificación OpenAPI (ReDoc):** `http://127.0.0.1:8000/redoc`

### 3. Frontend (Angular)
```bash
cd FRONTEND
npm install
npm start
```
* **Aplicación Web:** `http://localhost:4200`

---

## 📋 Endpoints Principales de la API

| Método | Ruta | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| `GET` | `/donaciones` | Listar todas las donaciones registradas | Público |
| `POST` | `/donaciones` | Registrar una nueva donación con validaciones | Requiere JWT |
| `PUT` | `/donaciones/{id}` | Actualizar un registro existente | Requiere JWT |
| `DELETE` | `/donaciones/{id}` | Eliminar permanentemente un registro | Requiere JWT |
| `GET` | `/comedores` | Listar comedores populares registrados (3FN) | Público |
| `POST` | `/comedores` | Registrar nuevo comedor popular | Requiere JWT |
| `GET` | `/categorias` | Listar categorías nutricionales (3FN) | Público |
| `POST` | `/auth/login` | Autenticación de usuario y obtención de token JWT | Público |
| `POST` | `/auth/registro` | Registro de nuevos usuarios administradores | Público |

---

## 🔑 Credenciales por Defecto

* **Usuario Administrador:** `admin@comedores.pe`
* **Contraseña:** `admin123`
