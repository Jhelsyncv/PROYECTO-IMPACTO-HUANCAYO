"""
Script de Inicialización y Migración a 3FN (Tercera Forma Normal)
Comedores Populares de Huancayo
"""
from database import engine, SessionLocal, Base
from models.usuario_modelo import UsuarioDB
from models.comedor_modelo import ComedorDB
from models.categoria_modelo import CategoriaDB
from models.donacion_modelo import DonacionDB
from sqlalchemy import text

def ejecutar_migracion_3fn():
    # 1. Asegurar la creación de tablas nuevas en PostgreSQL
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("=" * 60)
    print("INICIANDO MIGRACIÓN Y SEMBRADO DE BASE DE DATOS (3FN)")
    print("=" * 60)

    # 1.1 Si la tabla donaciones ya existía sin las columnas comedor_id o categoria_id, agregarlas con ALTER TABLE
    with engine.connect() as conn:
        for col_def in [
            "ALTER TABLE donaciones ADD COLUMN IF NOT EXISTS comedor_id INTEGER REFERENCES comedores(id) ON DELETE SET NULL;",
            "ALTER TABLE donaciones ADD COLUMN IF NOT EXISTS categoria_id INTEGER REFERENCES categorias(id) ON DELETE SET NULL;"
        ]:
            try:
                conn.execute(text(col_def))
                conn.commit()
            except Exception as e:
                print(f"Nota DDL: {e}")

    # 2. Sembrar Categorías si no existen
    categorias_iniciales = [
        ("Granos y Cereales", "Arroz, quinua, cebada, trigo, maíz, avena"),
        ("Lácteos", "Leche evaporada, queso, mantequilla, yogurt"),
        ("Cárnicos", "Pollo, carne de res, cerdo, pescado enlatado"),
        ("Verduras y Frutas", "Papa, zanahoria, cebolla, tomate, frutas de temporada"),
        ("Abarrotes", "Aceite vegetal, azúcar, fideos, sal, condimentos"),
        ("Líquidos y Bebidas", "Agua embotellada, jugos naturales, infusiones"),
        ("Otros", "Insumos varios no perecibles")
    ]

    for nombre, desc in categorias_iniciales:
        cat_existente = db.query(CategoriaDB).filter(CategoriaDB.nombre.ilike(nombre)).first()
        if not cat_existente:
            nueva_cat = CategoriaDB(nombre=nombre, descripcion=desc)
            db.add(nueva_cat)
    db.commit()
    print("✓ Categorías iniciales verificadas/sembradas.")

    # 3. Sembrar Comedores representativos de Huancayo si no existen
    comedores_iniciales = [
        ("Comedor Santa Rosa de Lima", "El Tambo", "Av. Huancavelica 1420", "María Quispe", "964112233"),
        ("Comedor San José", "Huancayo Centro", "Jr. Puno 340", "Elena Fernández", "964223344"),
        ("Comedor Virgen del Carmen", "Chilca", "Av. 9 de Diciembre 512", "Juana Romero", "964334455"),
        ("Comedor Sagrado Corazón", "Pilcomayo", "Av. Coronel Parra 210", "Rosa Huamán", "964445566"),
        ("Comedor Señor de los Milagros", "Huancán", "Jr. Real 104", "Carmen Torres", "964556677")
    ]

    for nombre, distrito, direccion, resp, tel in comedores_iniciales:
        com_existente = db.query(ComedorDB).filter(ComedorDB.nombre.ilike(nombre)).first()
        if not com_existente:
            nuevo_com = ComedorDB(
                nombre=nombre,
                distrito=distrito,
                direccion=direccion,
                responsable=resp,
                telefono=tel
            )
            db.add(nuevo_com)
    db.commit()
    print("✓ Comedores populares iniciales verificados/sembrados.")

    # 4. Vincular registros existentes de donaciones a 3FN
    donaciones = db.query(DonacionDB).all()
    actualizadas = 0

    for d in donaciones:
        cambio = False
        # Vincular Comedor ID si está en NULL
        if d.comedor_id is None and d.comedor:
            com = db.query(ComedorDB).filter(ComedorDB.nombre.ilike(d.comedor.strip())).first()
            if not com:
                # Crear comedor para el nombre registrado
                com = ComedorDB(
                    nombre=d.comedor.strip().title(),
                    distrito="Huancayo",
                    direccion="Sector Local"
                )
                db.add(com)
                db.commit()
                db.refresh(com)
            d.comedor_id = com.id
            cambio = True

        # Vincular Categoría ID si está en NULL
        if d.categoria_id is None:
            nombre_cat = (d.categoria or "Otros").strip()
            cat = db.query(CategoriaDB).filter(CategoriaDB.nombre.ilike(nombre_cat)).first()
            if not cat:
                cat = db.query(CategoriaDB).filter(CategoriaDB.nombre.ilike("Otros")).first()
            if cat:
                d.categoria_id = cat.id
                cambio = True

        if cambio:
            actualizadas += 1

    db.commit()
    print(f"✓ Registros de donaciones vinculados con Claves Foráneas: {actualizadas}/{len(donaciones)}")

    # 5. Resumen final
    total_comedores = db.query(ComedorDB).count()
    total_categorias = db.query(CategoriaDB).count()
    total_donaciones = db.query(DonacionDB).count()
    print("=" * 60)
    print("ESTADO FINAL DE BASE DE DATOS (3FN):")
    print(f" - Comedores registrados: {total_comedores}")
    print(f" - Categorías registradas: {total_categorias}")
    print(f" - Donaciones normalizadas: {total_donaciones}")
    print("=" * 60)
    db.close()

if __name__ == "__main__":
    ejecutar_migracion_3fn()
