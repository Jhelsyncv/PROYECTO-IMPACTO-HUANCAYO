# Sistema de Gestión de Donaciones - Comedores Huancayo

Aplicación web Full-Stack para el registro y administración de donaciones alimentarias destinadas a comedores populares en Huancayo.

## 🛠️ Tecnologías Utilizadas

- **Frontend:** Angular 18+, TypeScript, HTML5, CSS3.
- **Backend:** FastAPI (Python 3.10+), SQLAlchemy (ORM), Pydantic.
- **Base de Datos:** PostgreSQL.
- **Servidor Web / API:** Uvicorn.

---

## 🚀 Requisitos Previos

1. Tener instalado **Node.js** (v18+) y **Angular CLI**.
2. Tener instalado **Python 3.10+**.
3. Tener instalado **PostgreSQL 14+** y **pgAdmin 4**.

---

## ⚙️ Configuración del Proyecto

### 1. Base de Datos (PostgreSQL)

Crea la base de datos desde pgAdmin o tu terminal SQL:

```sql
CREATE DATABASE donaciones_db;

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Jhelsyn10@localhost:5432/donaciones_db"