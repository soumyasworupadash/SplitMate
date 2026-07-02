from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.activity import ActivityResponse
from app.services.activity_service import (
    get_group_activity,
    get_my_activity
)

router = APIRouter(
    prefix="/activity",
    tags=["Activity"]
)

@router.get(
    "/me",
    response_model=List[ActivityResponse]
)
def read_my_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_activity(
        current_user=current_user,
        db=db
    )

@router.get(
    "/{group_id}",
    response_model=List[ActivityResponse]
)
def read_activity(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_group_activity(
        group_id,
        db
    )