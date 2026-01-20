from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User
from app.schemas import RegisterRequest, RoleEnum
from app.utils import hash_password


def register_user(request: RegisterRequest, db: Session) -> User:

    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    new_user = User(
        email=request.email,
        username=request.username,
        password=hash_password(request.password),
        role=RoleEnum.operador.value
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(request: LoginRequest, db: Session) -> Token:

    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )
    
    access_token = create_access_token(
        data={
            "sub": user.id_user,
            "email": user.email,
            "role": user.role.value
        }
    )
    return Token(access_token=access_token, token_type="bearer")