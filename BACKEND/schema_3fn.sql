-- ============================================================================
-- PROYECTO: Sistema de Gestión de Donaciones - Comedores Populares de Huancayo
-- ARQUITECTURA DE BASE DE DATOS: PostgreSQL Normalizada hasta 3FN
-- ============================================================================

-- 1. CREACIÓN DE BASE DE DATOS (si es necesario)
-- CREATE DATABASE donaciones_db;

-- 2. TABLA DE USUARIOS DEL SISTEMA (1FN, 2FN, 3FN)
-- Almacena credenciales de acceso para autenticación JWT con Bcrypt
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    es_activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);

-- 3. TABLA DE CATEGORÍAS NUTRICIONALES (3FN)
-- Evita dependencias transitivas agrupando los alimentos
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(255) DEFAULT 'Insumos alimenticios'
);

CREATE INDEX IF NOT EXISTS idx_categorias_nombre ON categorias(nombre);

-- 4. TABLA DE COMEDORES POPULARES (3FN)
-- Entidad independiente para evitar redundancia de distritos, contactos y direcciones
CREATE TABLE IF NOT EXISTS comedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) UNIQUE NOT NULL,
    distrito VARCHAR(100) DEFAULT 'Huancayo',
    direccion VARCHAR(200) DEFAULT 'Sector Central',
    responsable VARCHAR(100) DEFAULT 'Coordinador de Comedor',
    telefono VARCHAR(50) DEFAULT '964000000',
    es_activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_comedores_nombre ON comedores(nombre);

-- 5. TABLA TRANSACCIONAL DE DONACIONES (3FN)
-- Cada donación referencia foráneamente a su Comedor y a su Categoría
CREATE TABLE IF NOT EXISTS donaciones (
    id SERIAL PRIMARY KEY,
    item VARCHAR(150) NOT NULL,
    cantidad_kg DOUBLE PRECISION NOT NULL CHECK (cantidad_kg > 0),
    comedor_id INTEGER REFERENCES comedores(id) ON DELETE SET NULL,
    categoria_id INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
    comedor VARCHAR(150),
    categoria VARCHAR(100) DEFAULT 'Otros',
    donante VARCHAR(150) DEFAULT 'Anónimo',
    fecha_registro TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_donaciones_comedor_id ON donaciones(comedor_id);
CREATE INDEX IF NOT EXISTS idx_donaciones_categoria_id ON donaciones(categoria_id);
CREATE INDEX IF NOT EXISTS idx_donaciones_fecha ON donaciones(fecha_registro);

-- ============================================================================
-- JUSTIFICACIÓN DE NORMALIZACIÓN HASTA 3FN:
-- 1FN: Todos los campos tienen valores atómicos, sin arreglos ni campos multivaluados.
-- 2FN: Cumple 1FN y cada atributo no clave depende funcionalmente de toda la clave primaria.
-- 3FN: Cumple 2FN y no existen dependencias funcionales transitivas entre atributos
--      no clave (los datos del comedor como distrito/dirección dependen de comedores.id,
--      no se repiten dentro de donaciones).
-- ============================================================================
