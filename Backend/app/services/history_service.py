from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.group import Group
from app.models.settlement import Settlement
from app.models.user import User


def get_user_history(
    user_id: int,
    db: Session
):
    result = {
        "expenses": [],
        "settlements": []
    }

    # Expenses created by the user
    expenses = (
        db.query(Expense)
        .filter(Expense.paid_by == user_id)
        .all()
    )

    for expense in expenses:

        group = (
            db.query(Group)
            .filter(Group.id == expense.group_id)
            .first()
        )

        result["expenses"].append(
            {
                "group": group.name,
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at
            }
        )

    # Settlements where the user is payer or receiver
    settlements = (
        db.query(Settlement)
        .filter(
            (Settlement.payer_id == user_id) |
            (Settlement.receiver_id == user_id)
        )
        .all()
    )

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

        group = (
            db.query(Group)
            .filter(Group.id == settlement.group_id)
            .first()
        )

        result["settlements"].append(
            {
                "group": group.name,
                "payer": payer.email,
                "receiver": receiver.email,
                "amount": settlement.amount,
                "settled_at": settlement.settled_at
            }
        )

    return result