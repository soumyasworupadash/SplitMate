from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.group_member import GroupMember
from app.services.balance_service import calculate_net_balances


def get_dashboard_summary(
    current_user,
    db: Session
):
    memberships = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id)
        .all()
    )

    total_owe = 0
    total_owed = 0

    highest_owed_group = None
    highest_owed_amount = 0

    for membership in memberships:

        balances = calculate_net_balances(
            membership.group_id,
            db
        )

        amount = balances.get(current_user.id, 0)

        if amount < 0:
            owe = abs(amount)
            total_owe += owe

            if owe > highest_owed_amount:
                highest_owed_amount = owe

                group = (
                    db.query(Group)
                    .filter(Group.id == membership.group_id)
                    .first()
                )

                if group:
                    highest_owed_group = group.name

        else:
            total_owed += amount

    return {
        "total_owe": round(total_owe, 2),
        "total_owed": round(total_owed, 2),
        "net_balance": round(total_owed - total_owe, 2),
        "group_count": len(memberships),
        "highest_owed_group": highest_owed_group
    }