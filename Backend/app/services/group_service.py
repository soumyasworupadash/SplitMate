from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User
from app.schemas.group import GroupCreate
from app.services.activity_service import log_activity
from app.services.balance_service import calculate_net_balances
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.settlement import Settlement
from app.models.activity_log import Activity
def create_group(
    group: GroupCreate,
    current_user: User,
    db: Session
):
    # Check if a group with the same name already exists for this user
    existing_group = (
        db.query(Group)
        .filter(
            Group.owner_id == current_user.id,
            Group.name == group.name
        )
        .first()
    )

    if existing_group:
        raise HTTPException(
            status_code=400,
            detail="You already have a group with this name."
        )

    # Create the group
    new_group = Group(
        name=group.name,
        owner_id=current_user.id
    )

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    # Automatically add the owner as a member
    owner_member = GroupMember(
        group_id=new_group.id,
        user_id=current_user.id
    )

    db.add(owner_member)
    db.commit()

    return new_group


def get_groups(current_user: User, db: Session):

    groups = (
        db.query(Group)
        .join(
            GroupMember,
            Group.id == GroupMember.group_id
        )
        .filter(
            GroupMember.user_id == current_user.id
        )
        .all()
    )

    return groups


def add_member(
    group_id: int,
    email: str,
    current_user: User,
    db: Session
):
    # Check if group exists
    group = (
        db.query(Group)
        .filter(Group.id == group_id)
        .first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found."
        )

    # Only owner can add members
    if group.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the group owner can add members."
        )

    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # Check if already a member
    existing_member = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user.id
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this group."
        )

    # Add member
    member = GroupMember(
        group_id=group_id,
        user_id=user.id
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    log_activity(
        group_id=group_id,
        user_id=current_user.id,
        action="Member Added",
        description=f"{current_user.email} added {user.email} to the group.",
        db=db
    )



    return member

def remove_member(
    group_id: int,
    user_id: int,
    current_user: User,
    db: Session
):
    # Check group exists
    group = (
        db.query(Group)
        .filter(Group.id == group_id)
        .first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found."
        )

    # Only owner can remove members
    if group.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the group owner can remove members."
        )

    # Owner cannot remove themselves
    if user_id == group.owner_id:
        raise HTTPException(
            status_code=400,
            detail="Group owner cannot be removed."
        )

    member = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found."
        )
    balances = calculate_net_balances(
        group_id=group_id,
        db=db
    )
    member_balance = round(
        balances.get(user_id, 0),
        2
    )
    if member_balance != 0:
        raise HTTPException(
            status_code=400,
            detail="Member cannot be removed because they have an outstanding balance."
    )


    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    db.delete(member)
    db.commit()

    log_activity(
        group_id=group_id,
        user_id=current_user.id,
        action="Member Removed",
        description=f"{current_user.email} removed {user.email} from the group.",
        db=db
    )

    return {
        "message": "Member removed successfully."
    }

def delete_group(
    group_id: int,
    current_user: User,
    db: Session
):
    # Check group exists
    group = (
        db.query(Group)
        .filter(Group.id == group_id)
        .first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found."
        )

    # Only owner can delete
    if group.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the group owner can delete this group."
        )

    # Get all expense IDs
    expense_ids = [
        expense.id
        for expense in db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    ]

    # Delete expense splits
    if expense_ids:
        (
            db.query(ExpenseSplit)
            .filter(
                ExpenseSplit.expense_id.in_(expense_ids)
            )
            .delete(synchronize_session=False)
        )

    # Delete expenses
    (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .delete(synchronize_session=False)
    )

    # Delete settlements
    (
        db.query(Settlement)
        .filter(Settlement.group_id == group_id)
        .delete(synchronize_session=False)
    )

    # Delete activities
    (
        db.query(Activity)
        .filter(Activity.group_id == group_id)
        .delete(synchronize_session=False)
    )

    # Delete group members
    (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id)
        .delete(synchronize_session=False)
    )

    # Delete group
    db.delete(group)

    db.commit()

    return {
        "message": "Group deleted successfully."
    }

def get_group_members(
    group_id: int,
    current_user: User,
    db: Session
):
    # Check if group exists
    group = (
        db.query(Group)
        .filter(Group.id == group_id)
        .first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found."
        )

    # Check if the current user is a member of the group
    member = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == current_user.id
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this group."
        )

    members = (
        db.query(User.id, User.email)
        .join(
            GroupMember,
            User.id == GroupMember.user_id
        )
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    return members