from pydantic import BaseModel, EmailStr, Field


# ============================================
# REQUEST SCHEMAS
# ============================================

class LoginRequest(BaseModel):
    """POST /auth/login"""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """POST /auth/register"""
    username: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


# ============================================
# RESPONSE SCHEMAS
# ============================================

class Token(BaseModel):
    """Respuesta login exitoso"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos dentro del JWT (uso interno)"""
    user_id: int | None = None
    email: str | None = None
    role: str | None = None