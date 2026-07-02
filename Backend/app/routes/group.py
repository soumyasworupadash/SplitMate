from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.group import (
    GroupCreate,
    GroupResponse,
    AddMemberRequest,
    GroupMemberResponse
)
from app.schemas.user import UserResponse
from app.services.group_service import (
    create_group,
    get_groups,
    add_member,
    remove_member,
    delete_group,
    get_group_members
)
from typing import List

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


@router.post("/", response_model=GroupResponse)
def create_new_group(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_group(
        group=group,
        current_user=current_user,
        db=db
    )

@router.get("/", response_model=List[GroupResponse])
def get_all_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_groups(
        current_user=current_user,
        db=db
    )

@router.post(
    "/{group_id}/members",
    response_model=GroupMemberResponse
)
def add_group_member(
    group_id: int,
    member: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_member(
        group_id=group_id,
        email=member.email,
        current_user=current_user,
        db=db
    )
@router.delete("/{group_id}/members/{user_id}")
def remove_group_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return remove_member(
        group_id=group_id,
        user_id=user_id,
        current_user=current_user,
        db=db
    )

@router.delete("/{group_id}")
def delete_existing_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_group(
        group_id=group_id,
        current_user=current_user,
        db=db
    )
@router.get(
    "/{group_id}/members",
    response_model=List[UserResponse]
)
def get_members(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_group_members(
        group_id=group_id,
        current_user=current_user,
        db=db
    )
