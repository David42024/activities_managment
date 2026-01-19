from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    operador = "operador"

class User(Base):
    __tablename__ = "users"
    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.operador, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    activities_assigned = relationship(
        "Activity",
        back_populates="assigned_user",
        foreign_keys="Activity.id_user"
    )
    activities_created = relationship(
        "Activity",
        back_populates="creator",
        foreign_keys="Activity.created_by"
    )
    historical_records = relationship(
        "Historical",
        back_populates="user"
    )

    def __repr__(self):
        return f"<User(id={self.id_user}, email='{self.email}', role='{self.role}')>"