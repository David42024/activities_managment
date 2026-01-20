# app/services/category.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import User, Category
from app.schemas import CategoryCreate, CategoryUpdate, CategoryList


def get_all(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False
) -> CategoryList:
    """Lista todas las categorías"""
    
    query = db.query(Category)
    
    # Solo admins ven inactivas
    if not include_inactive or current_user.role.value != "admin":
        query = query.filter(Category.is_active == True)
    
    total = query.count()
    categories = query.offset(skip).limit(limit).all()
    
    return CategoryList(categories=categories, total=total)


def get_by_id(db: Session, category_id: int, current_user: User) -> Category:
    """Obtiene una categoría por ID"""
    
    category = db.query(Category).filter(Category.id_category == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Solo admins ven inactivas
    if not category.is_active and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    return category


def create(db: Session, request: CategoryCreate) -> Category:
    """Crea una nueva categoría"""
    
    # Verificar nombre único
    if db.query(Category).filter(Category.name == request.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre"
        )
    
    new_category = Category(**request.model_dump())
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category


def update(db: Session, category_id: int, request: CategoryUpdate) -> Category:
    """Actualiza una categoría"""
    
    category = db.query(Category).filter(Category.id_category == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Verificar nombre único si se está cambiando
    if request.name and request.name != category.name:
        if db.query(Category).filter(Category.name == request.name).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una categoría con ese nombre"
            )
    
    # Actualizar
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return category


def delete(db: Session, category_id: int, hard_delete: bool = False) -> None:
    """Elimina una categoría"""
    
    category = db.query(Category).filter(Category.id_category == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    if hard_delete:
        db.delete(category)
    else:
        category.is_active = False
    
    db.commit()