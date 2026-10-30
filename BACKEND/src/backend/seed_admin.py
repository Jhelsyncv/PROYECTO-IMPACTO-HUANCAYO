from database import SessionLocal, engine, Base
from models.usuario_modelo import UsuarioDB
from services.auth_servicio import obtener_password_hash

# Asegurar que existan las tablas
Base.metadata.create_all(bind=engine)

def crear_usuario_admin():
    db = SessionLocal()
    email_admin = "admin@comedores.pe"
    
    # Verificar si ya existe
    usuario_existente = db.query(UsuarioDB).filter(UsuarioDB.email == email_admin).first()
    if usuario_existente:
        print("El usuario administrador ya existe.")
        db.close()
        return

    # Crear nuevo administrador
    nuevo_admin = UsuarioDB(
        nombre="Administrador General",
        email=email_admin,
        password_hash=obtener_password_hash("admin123"),
        es_activo=True
    )
    
    db.add(nuevo_admin)
    db.commit()
    print("Usuario administrador creado exitosamente:")
    print(" Email: admin@comedores.pe")
    print(" Contraseña: admin123")
    db.close()

if __name__ == "__main__":
    crear_usuario_admin()