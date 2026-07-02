from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.settlement import Settlement
from app.models.user import User
from app.schemas.settlement import SettlementCreate
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.services.activity_service import log_activity

def get_outstanding_balance(
    group_id: int,
    payer_id: int,
    receiver_id: int,
    db: Session
):
    total_owed = 0

    expenses = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    for expense in expenses:

        if expense.paid_by != receiver_id:
            continue

        split = (
            db.query(ExpenseSplit)
            .filter(
                ExpenseSplit.expense_id == expense.id,
                ExpenseSplit.user_id == payer_id
            )
            .first()
        )

        if split:
            total_owed += split.amount

    settlements = (
        db.query(Settlement)
        .filter(
            Settlement.group_id == group_id,
            Settlement.payer_id == payer_id,
            Settlement.receiver_id == receiver_id
        )
        .all()
    )

    total_paid = sum(s.amount for s in settlements)

    return round(total_owed - total_paid, 2)





def create_settlement(
    settlement: SettlementCreate,
    current_user: User,
    db: Session
):
    # Check group exists
    group = (
        db.query(Group)
        .filter(Group.id == settlement.group_id)
        .first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found."
        )
    # # For Preventing self-settlement
    if current_user.id == settlement.receiver_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot settle with yourself."
    )

    # Check payer belongs to group
    payer = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == settlement.group_id,
            GroupMember.user_id == current_user.id
        )
        .first()
    )

    if payer is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this group."
        )

    # Check receiver belongs to group
    receiver = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == settlement.group_id,
            GroupMember.user_id == settlement.receiver_id
        )
        .first()
    )

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver is not a member of this group."
        )
    if settlement.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Settlement amount must be greater than zero."
        )
    balance = get_outstanding_balance(
    settlement.group_id,
    current_user.id,
    settlement.receiver_id,
    db
    )

    if balance <= 0:
        raise HTTPException(
            status_code=400,
            detail="No outstanding balance exists."
        )
    if settlement.amount > balance:
        raise HTTPException(
            status_code=400,
            detail="Settlement amount exceeds outstanding balance."
        )

    new_settlement = Settlement(
        group_id=settlement.group_id,
        payer_id=current_user.id,
        receiver_id=settlement.receiver_id,
        amount=settlement.amount
    )

    db.add(new_settlement)
    db.commit()
    db.refresh(new_settlement)

    receiver_user = (
        db.query(User)
        .filter(User.id == settlement.receiver_id)
        .first()
    )

    log_activity(
        group_id=new_settlement.group_id,
        user_id=current_user.id,
        action="Settlement Recorded",
        description=f"{current_user.email} settled ₹{new_settlement.amount} with {receiver_user.email}.",
        db=db
    )



    return new_settlement


def get_settlements(
    group_id: int,
    db: Session
):
    settlements = (
        db.query(Settlement)
        .filter(Settlement.group_id == group_id)
        .all()
    )

    result = []

    for settlement in settlements:

        payer = (
            db.query(User)
            .filter(User.id == settlement.payer_id)
            .first()
        )

        receiver = (
            db.query(User)
            .filter(User.id == settlement.receiver_id)
            .first()
        )

        result.append(
            {
                "payer": payer.email,
                "receiver": receiver.email,
                "amount": settlement.amount,
                "settled_at": settlement.settled_at
            }
        )

    return result