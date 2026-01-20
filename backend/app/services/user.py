from app.schemas import UserList
from app.models import User
from sqlalchemy.orm import Session

def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    include_inactive: bool = False
) -> UserList:
    """Lista todos los usuarios"""
    
    query = db.query(User)
    
    if not include_inactive:
        query = query.filter(User.is_active == True)
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return UserList(
        users=users,
        total=total,
        page=(skip // limit) + 1,
        per_page=limit
    )