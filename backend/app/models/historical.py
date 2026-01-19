from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Historical(Base):
    __tablename__ = "historical"

    id_historical = Column(Integer, primary_key=True, index=True)
    
    entity = Column(String(50), nullable=False, index=True) 
    entity_id = Column(Integer, nullable=False, index=True) 
    
    action = Column(String(20), nullable=False) 
    modified_field = Column(String(50), nullable=True) 
    previous_value = Column(Text, nullable=True) 
    new_value = Column(Text, nullable=True) 
    
    id_user = Column(
        Integer,
        ForeignKey("users.id_user", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    user = relationship(
        "User",
        back_populates="historical_records"
    )
    
    
    def __repr__(self):
        return f"<Historical(id={self.id_historical}, entity='{self.entity}', action='{self.action}')>"