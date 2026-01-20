from fastapi import APIRouter
from app.schemas import UserList, UserResponse, UserUpdate, UserChangePassword
from app.services import user as user_service
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import get_current_admin, get_current_user
from app.models import User
from fastapi import Query, Depends
from fastapi import status

router = APIRouter()

@router.get("", response_model=UserList)
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin) #muy importante
):
    return user_service.get_all(db, current_user, skip, limit, include_inactive)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) #muy importante
):
    return user_service.get_by_id(db, user_id, current_user)

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) #muy importante
):
    return user_service.update(db, user_id, request, current_user)

@router.patch("/{user_id}/password", response_model=UserResponse)
def change_password(
    user_id: int,
    request: UserChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.change_password(db, user_id, request, current_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    hard_delete: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Elimina un usuario (solo admin)"""
    user_service.delete(db, user_id, current_user, hard_delete)
    return None