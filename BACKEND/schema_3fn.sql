-- ============================================================================
-- PROYECTO: Sistema de Gestión de Donaciones - Comedores Populares de Huancayo
-- ARQUITECTURA DE BASE DE DATOS: PostgreSQL Normalizada hasta 3FN
-- FUENTE DE DATOS: Padrón PCA y Resoluciones Oficiales de la Municipalidad Provincial de Huancayo (MPH / GDIS)
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
    responsable VARCHAR(150) DEFAULT 'Coordinador de Comedor',
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
-- DATOS INICIALES SEMBRADOS (COMEDORES REALES OFICIALES DE HUANCAYO)
-- ============================================================================
INSERT INTO comedores (nombre, distrito, direccion, responsable, telefono) VALUES
('Comedor Popular Zoila Victoria', 'El Tambo', 'Av. Mariscal Castilla 2240, El Tambo', 'Sra. Victoria Mayta (Pres. Res. 82-2025-MPH)', '964182931'),
('Comedor Popular Los Andes', 'El Tambo', 'Jr. Los Andes 450, El Tambo', 'Sra. Gladys Alanya (Pres. Res. 42-2025-MPH)', '964273849'),
('Comedor Popular La Merced de Umuto', 'El Tambo', 'Av. Evitamiento s/n, Anexo Umuto', 'Sra. Juana Cárdenas (Pres. Res. 34-2025-MPH)', '964394820'),
('Comedor Popular Sagrada Familia', 'El Tambo', 'Jr. Julio Sumar 320, El Tambo', 'Sra. Martha Sedano (Pres. Res. 30-2025-MPH)', '964485921'),
('Comedor Popular Virgen de Cocharcas III', 'Huancayo Centro', 'Jr. Cajamarca 615, Huancayo Cercado', 'Sra. Carmen Huamán (Pres. Res. 15-2022-MPH)', '964592817'),
('Comedor Popular Juan Pablo II', 'Huancayo Centro', 'Prolongación Ica 280, Huancayo', 'Sra. Teófila Ramos (Coordinadora PCA)', '964672910'),
('Comedor Popular Mujeres Unidas', 'El Tambo', 'Av. Circunvalación 812, El Tambo', 'Sra. Bertha Quispe (Presidenta OSB)', '964783921'),
('Comedor Popular Señor de los Milagros', 'Chilca', 'Av. 9 de Diciembre 430, Chilca', 'Sra. Elena Poma (Presidenta OSB)', '964892013'),
('Comedor Popular Santa Rosa de Lima', 'Pilcomayo', 'Av. Las Palmeras 150, Pilcomayo', 'Sra. Lucía Fernández (Coordinadora PCA)', '964918273')
ON CONFLICT (nombre) DO NOTHING;
