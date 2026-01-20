from pydantic import BaseModel
from datetime import datetime

class HistoricalBase(BaseModel):
    entity: str
    entity_id: int
    action: str
    modified_field: str | None = None
    previous_value: str | None = None
    new_value: str | None = None


class HistoricalResponse(HistoricalBase):
    """Registro de auditoría"""
    id_historical: int
    id_user: int
    created_at: datetime

    class Config:
        from_attributes = True


class HistoricalWithUser(HistoricalBase):
    """Con datos del usuario que hizo el cambio"""
    id_historical: int
    created_at: datetime
    user: dict  # Evita import circular

    class Config:
        from_attributes = True


class HistoricalList(BaseModel):
    """Lista de auditoría"""
    records: list[HistoricalResponse]
    total: int