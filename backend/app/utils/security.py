from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import TokenData

# ============================================
# PASSWORD HASHING
# ============================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea una contraseña"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================
# JWT TOKENS
# ============================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token.
    
    Uso:
        token = create_access_token({"sub": user.id_user, "email": user.email})
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        print(f"Payload: {payload}")  # Debug
        
        user_id = payload.get("sub")
        email = payload.get("email")
        role = payload.get("role")
        
        print(f"user_id: {user_id}, email: {email}, role: {role}")  # Debug
        
        if user_id is None:
            return None
            
        return TokenData(user_id=int(user_id), email=email, role=role)
        
    except JWTError as e:
        print(f"JWTError: {e}")  # Debug - ¿Hay error aquí?
        return None


# ============================================
# DEPENDENCIES: Para inyectar en endpoints
# ============================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    
    print(f"Token recibido: {token[:50]}...")  # Debug
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_token(token)
    print(f"Token decodificado: {token_data}")  # Debug
    
    if token_data is None:
        print("Token data es None!")  # Debug
        raise credentials_exception
    
    user = db.query(User).filter(User.id_user == token_data.user_id).first()
    print(f"Usuario encontrado: {user}")  # Debug
    
    # ...resto del código
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )
    
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica que el usuario sea admin.
    
    Uso:
        @router.delete("/users/{id}")
        def delete_user(current_user: User = Depends(get_current_admin)):
            ...
    """
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador"
        )
    return current_user