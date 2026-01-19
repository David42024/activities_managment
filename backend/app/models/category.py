from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Category(Base):
    __tablename__ = "category"
    
    id_category = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True) 
    color = Column(String(7), nullable=False, default="#3498db")  # Formato: #RRGGBB
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # ============================================
    # RELACIÓN: Una categoría tiene muchas actividades
    # ============================================
    # lazy="dynamic": No carga las actividades hasta que las pidas
    # Útil cuando una categoría puede tener miles de actividades
    
    activities = relationship(
        "Activity",
        back_populates="category",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return f"<Category(id={self.id_category}, name='{self.name}')>"