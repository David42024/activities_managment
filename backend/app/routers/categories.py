# app/routers/categories.py

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryList
from app.services import category as category_service
from app.utils import get_current_user, get_current_admin

router = APIRouter()


@router.get("", response_model=CategoryList)
def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todas las categorías"""
    return category_service.get_all(db, current_user, skip, limit, include_inactive)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene una categoría por ID"""
    return category_service.get_by_id(db, category_id, current_user)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Crea una nueva categoría (solo admin)"""
    return category_service.create(db, request)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Actualiza una categoría (solo admin)"""
    return category_service.update(db, category_id, request)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    hard_delete: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Elimina una categoría (solo admin)"""
    category_service.delete(db, category_id, hard_delete)
    return None