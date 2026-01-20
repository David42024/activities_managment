# app/services/activity.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from datetime import date

from app.models import User, Activity, Category
from app.models.activity import ActivityStateEnum, PriorityEnum
from app.schemas import ActivityCreate, ActivityUpdate, ActivityChangeState, ActivityList


# ============================================
# VALIDACIÓN DE TRANSICIONES DE ESTADO
# ============================================

VALID_TRANSITIONS = {
    "pendiente": ["en_progreso", "cancelada"],
    "en_progreso": ["bloqueada", "completada", "cancelada"],
    "bloqueada": ["en_progreso", "cancelada"],
    "completada": ["en_progreso"],
    "cancelada": [],
}


def validate_state_transition(current_state: str, new_state: str) -> bool:
    """Verifica si una transición de estado es válida"""
    return new_state in VALID_TRANSITIONS.get(current_state, [])


# ============================================
# SERVICIOS
# ============================================

def get_all(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 20,
    state: ActivityStateEnum | None = None,
    priority: PriorityEnum | None = None,
    id_category: int | None = None,
    id_user: int | None = None,
    due_date_from: date | None = None,
    due_date_to: date | None = None,
    search: str | None = None,
    include_inactive: bool = False
) -> ActivityList:
    """Lista actividades con filtros"""
    
    query = db.query(Activity)
    
    # Operadores solo ven sus actividades
    if current_user.role.value != "admin":
        query = query.filter(
            or_(
                Activity.id_user == current_user.id_user,
                Activity.created_by == current_user.id_user
            )
        )
    
    # Soft delete
    if not include_inactive:
        query = query.filter(Activity.is_active == True)
    
    # Filtros
    if state:
        query = query.filter(Activity.state == state)
    
    if priority:
        query = query.filter(Activity.priority == priority)
    
    if id_category:
        query = query.filter(Activity.id_category == id_category)
    
    if id_user:
        query = query.filter(Activity.id_user == id_user)
    
    if due_date_from:
        query = query.filter(Activity.due_date >= due_date_from)
    
    if due_date_to:
        query = query.filter(Activity.due_date <= due_date_to)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Activity.title.ilike(search_term),
                Activity.description.ilike(search_term)
            )
        )
    
    # Ordenar
    query = query.order_by(Activity.due_date.asc().nullslast(), Activity.priority.desc())
    
    total = query.count()
    activities = query.offset(skip).limit(limit).all()
    
    return ActivityList(
        activities=activities,
        total=total,
        page=(skip // limit) + 1,
        per_page=limit
    )


def get_by_id(db: Session, activity_id: int, current_user: User) -> Activity:
    """Obtiene una actividad por ID"""
    
    activity = db.query(Activity).filter(Activity.id_activity == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    
    # Permisos
    if current_user.role.value != "admin":
        if activity.id_user != current_user.id_user and activity.created_by != current_user.id_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta actividad"
            )
    
    return activity


def create(db: Session, request: ActivityCreate, current_user: User) -> Activity:
    """Crea una nueva actividad"""
    
    # Verificar categoría
    if request.id_category:
        category = db.query(Category).filter(
            Category.id_category == request.id_category,
            Category.is_active == True
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoría no encontrada o inactiva"
            )
    
    new_activity = Activity(
        **request.model_dump(),
        id_user=current_user.id_user,
        created_by=current_user.id_user,
        state=ActivityStateEnum.pendiente
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    
    return new_activity


def update(db: Session, activity_id: int, request: ActivityUpdate, current_user: User) -> Activity:
    """Actualiza una actividad"""
    
    activity = db.query(Activity).filter(Activity.id_activity == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    
    # Permisos
    if current_user.role.value != "admin":
        if activity.created_by != current_user.id_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el creador o un admin puede editar esta actividad"
            )
    
    # Verificar categoría
    if request.id_category:
        category = db.query(Category).filter(
            Category.id_category == request.id_category,
            Category.is_active == True
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoría no encontrada o inactiva"
            )
    
    # Verificar usuario asignado
    if request.id_user:
        assigned_user = db.query(User).filter(
            User.id_user == request.id_user,
            User.is_active == True
        ).first()
        if not assigned_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario asignado no encontrado o inactivo"
            )
    
    # Actualizar
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


def change_state(
    db: Session,
    activity_id: int,
    request: ActivityChangeState,
    current_user: User
) -> Activity:
    """Cambia el estado de una actividad"""
    
    activity = db.query(Activity).filter(Activity.id_activity == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    
    # Permisos
    if current_user.role.value != "admin":
        if activity.id_user != current_user.id_user and activity.created_by != current_user.id_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para cambiar el estado de esta actividad"
            )
    
    # Validar transición
    current_state = activity.state.value
    new_state = request.state.value
    
    if not validate_state_transition(current_state, new_state):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transición inválida: {current_state} → {new_state}. "
                   f"Permitidas: {VALID_TRANSITIONS[current_state]}"
        )
    
    activity.state = request.state
    
    db.commit()
    db.refresh(activity)
    
    return activity


def delete(db: Session, activity_id: int, current_user: User, hard_delete: bool = False) -> None:
    """Elimina una actividad"""
    
    activity = db.query(Activity).filter(Activity.id_activity == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    
    # Permisos
    if current_user.role.value != "admin":
        if activity.created_by != current_user.id_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el creador o un admin puede eliminar esta actividad"
            )
    
    if hard_delete and current_user.role.value == "admin":
        db.delete(activity)
    else:
        activity.is_active = False
    
    db.commit()