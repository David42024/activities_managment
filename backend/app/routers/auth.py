from fastapi import APIRouter
from app.schemas.auth import RegisterRequest, UserResponse
from app.services.auth import register
from fastapi import status
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.services import auth as auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_endpoint(request: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(request, db)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user_endpoint(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(request, db)
