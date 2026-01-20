from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    operador = "operador"

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    role: RoleEnum = Field(default=RoleEnum.operador)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = None
    role: RoleEnum | None = None
    is_active: bool | None = None

class UserChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6, max_length=100)

class UserResponse(UserBase):
    """Usuario sin password"""
    id_user: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserList(BaseModel):
    """Lista paginada"""
    users: list[UserResponse]
    total: int
    page: int
    per_page: int