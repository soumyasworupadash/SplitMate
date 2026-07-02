from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.services.history_service import get_user_history

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/")
def read_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_history(
        current_user.id,
        db
    )