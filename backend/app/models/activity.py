from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base

class ActivityStateEnum(str, enum.Enum):
    """
    Máquina de estados:
    pendiente → en_progreso → completada
                    ↓
               bloqueada
                    ↓
               cancelada
    """
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    bloqueada = "bloqueada"
    completada = "completada"
    cancelada = "cancelada"


class PriorityEnum(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    urgente = "urgente"


class Activity(Base):
    __tablename__ = "activity"
    id_activity = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    state = Column(
        Enum(ActivityStateEnum),
        nullable=False,
        default=ActivityStateEnum.pendiente,
        index=True
    )
    priority = Column(
        Enum(PriorityEnum),
        nullable=False,
        default=PriorityEnum.media,
        index=True
    )
    
    due_date = Column(Date, nullable=True, index=True)
    
    id_user = Column(
        Integer,
        ForeignKey("users.id_user", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    id_category = Column(
        Integer,
        ForeignKey("category.id_category", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    created_by = Column(
        Integer,
        ForeignKey("users.id_user", ondelete="RESTRICT"),
        nullable=False
    )
    
    # Soft delete
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    assigned_user = relationship(
        "User",
        back_populates="activities_assigned",
        foreign_keys=[id_user]
    )
    
    # activity.creator → objeto User
    creator = relationship(
        "User",
        back_populates="activities_created",
        foreign_keys=[created_by]
    )
    
    # activity.category → objeto Category
    category = relationship(
        "Category",
        back_populates="activities"
    )
    
    def __repr__(self):
        return f"<Activity(id={self.id_activity}, title='{self.title}', state='{self.state}')>"