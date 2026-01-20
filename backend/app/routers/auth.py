from fastapi import APIRouter
from app.services import auth as auth_service
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import status
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas import RegisterRequest, UserResponse, Token, LoginRequest
from app.utils import get_current_user
from app.models import User
from app.services import auth as auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_endpoint(request: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(request, db)

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_user_endpoint(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(request, db)

@router.post("/token", response_model=Token)
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login para Swagger UI (form-data)"""
    return auth_service.login_with_form(form_data.username, form_data.password, db)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Devuelve el usuario autenticado"""
    return current_user