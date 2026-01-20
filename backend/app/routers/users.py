from fastapi import APIRouter
from app.schemas import UserList
from app.services import user as user_service
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import get_current_admin
from app.models import User
from fastapi import Query, Depends

router = APIRouter()

@router.get("", response_model=UserList)
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin) #muy importante
):
    return user_service.get_all(db, skip, limit, include_inactive)