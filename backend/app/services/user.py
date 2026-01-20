from app.schemas import UserList, UserUpdate, UserChangePassword
from app.models import User
from sqlalchemy.orm import Session
from app.utils import verify_password, hash_password, get_current_user, get_current_admin
from fastapi import HTTPException, status

def get_all(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 20,
    include_inactive: bool = False
) -> UserList:
    """Lista todos los usuarios"""
    
    query = db.query(User)
    
    if not include_inactive:
        query = query.filter(User.is_active == True)
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return UserList(
        users=users,
        total=total,
        page=(skip // limit) + 1,
        per_page=limit
    )

def get_by_id(
    db: Session,
    user_id: int,
    current_user: User
) -> User:
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user

def update(
    db: Session,
    user_id: int,
    request: UserUpdate,
    current_user: User
) -> User:
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este usuario")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if current_user.role.value != "admin":
        if current_user.id_user != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para editar este usuario"
            )
        if request.role is not None or request.is_active is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para cambiar rol o estado"
            )

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar email único
    if request.email and request.email != user.email:
        if db.query(User).filter(User.email == request.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso"
            )
    
    # Verificar username único
    if request.username and request.username != user.username:
        if db.query(User).filter(User.username == request.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso"
            )

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

def change_password(
    db: Session,
    user_id: int,
    request: UserChangePassword,
    current_user: User
) -> User:

    if current_user.role.value != "admin" and current_user.id_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para cambiar esta contraseña"
        )
    
    user = db.query(User).filter(User.id_user == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar contraseña actual (excepto admin)
    if current_user.role.value != "admin":
        if not verify_password(request.current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
    
    user.password = hash_password(request.new_password)
    
    db.commit()
    db.refresh(user)
    
    return user

def delete(db: Session, user_id: int, current_user: User, hard_delete: bool = False) -> None:
    """Elimina un usuario"""
    
    if current_user.id_user == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminarte a ti mismo"
        )
    
    user = db.query(User).filter(User.id_user == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if hard_delete:
        db.delete(user)
    else:
        user.is_active = False
    
    db.commit()