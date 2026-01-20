# app/routers/activities.py

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models import User
from app.models.activity import ActivityStateEnum, PriorityEnum
from app.schemas import ActivityCreate, ActivityUpdate, ActivityChangeState, ActivityResponse, ActivityList
from app.services import activity as activity_service
from app.utils import get_current_user

router = APIRouter()


@router.get("", response_model=ActivityList)
def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    state: ActivityStateEnum | None = None,
    priority: PriorityEnum | None = None,
    id_category: int | None = None,
    id_user: int | None = None,
    due_date_from: date | None = None,
    due_date_to: date | None = None,
    search: str | None = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista actividades con filtros"""
    return activity_service.get_all(
        db, current_user, skip, limit,
        state, priority, id_category, id_user,
        due_date_from, due_date_to, search, include_inactive
    )


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene una actividad por ID"""
    return activity_service.get_by_id(db, activity_id, current_user)


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    request: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una nueva actividad"""
    return activity_service.create(db, request, current_user)


@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: int,
    request: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza una actividad"""
    return activity_service.update(db, activity_id, request, current_user)


@router.patch("/{activity_id}/state", response_model=ActivityResponse)
def change_activity_state(
    activity_id: int,
    request: ActivityChangeState,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cambia el estado de una actividad"""
    return activity_service.change_state(db, activity_id, request, current_user)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: int,
    hard_delete: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina una actividad"""
    activity_service.delete(db, activity_id, current_user, hard_delete)
    return None