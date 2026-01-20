from pydantic import BaseModel, Field
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = None
    color: str = Field(default="#3498db", pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: bool | None = None

class CategoryResponse(CategoryBase):
    """Categoría completa"""
    id_category: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryList(BaseModel):
    """Lista de categorías"""
    categories: list[CategoryResponse]
    total: int