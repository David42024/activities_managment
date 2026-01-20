from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum


class ActivityStateEnum(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    bloqueada = "bloqueada"
    completada = "completada"
    cancelada = "cancelada"


class PriorityEnum(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    urgente = "urgente"

class ActivityBase(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    priority: PriorityEnum = PriorityEnum.media
    due_date: date | None = None
    id_user: int | None = None
    id_category: int | None = None

class ActivityCreate(ActivityBase):
    """POST /activities"""
    pass


class ActivityUpdate(BaseModel):
    """PATCH /activities/{id}"""
    title: str | None = Field(None, min_length=2, max_length=200)
    description: str | None = None
    priority: PriorityEnum | None = None
    due_date: date | None = None
    id_user: int | None = None
    id_category: int | None = None


class ActivityChangeState(BaseModel):
    """PATCH /activities/{id}/state"""
    state: ActivityStateEnum

class ActivityResponse(ActivityBase):
    """Actividad simple"""
    id_activity: int
    state: ActivityStateEnum
    created_by: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActivityList(BaseModel):
    """Lista paginada"""
    activities: list[ActivityResponse]
    total: int
    page: int
    per_page: int

class ActivityDetailResponse(BaseModel):
    """Actividad con usuario y categoría expandidos"""
    id_activity: int
    title: str
    description: str | None
    state: ActivityStateEnum
    priority: PriorityEnum
    due_date: date | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Relaciones como dict para evitar imports circulares
    assigned_user: dict | None = None
    category: dict | None = None
    creator: dict

    class Config:
        from_attributes = True

class ActivityFilters(BaseModel):
    """Query params para filtrar"""
    state: ActivityStateEnum | None = None
    priority: PriorityEnum | None = None
    id_category: int | None = None
    id_user: int | None = None
    due_date_from: date | None = None
    due_date_to: date | None = None
    search: str | None = None