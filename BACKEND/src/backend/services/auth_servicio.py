import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Cargar variables de entorno con valores por defecto seguros
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_super_segura_comedores_huancayo")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_password_hash(password: str) -> str:
    """Genera el hash seguro de la contraseña usando bcrypt."""
    return pwd_context.hash(password)

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash almacenado."""
    return pwd_context.verify(password_plano, password_hash)

def crear_token_acceso(data: dict) -> str:
    """Genera un token JWT firmado con expiración configurada."""
    a_codificar = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    a_codificar.update({"exp": expiracion})
    return jwt.encode(a_codificar, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> str:
    """Dependencia para validar el token JWT y extraer el email del usuario autenticado."""
    expire_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesión expirada o credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise expire_exception
        return email
    except JWTError:
        raise expire_exception
