from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.settlement import Settlement
from app.models.user import User
from app.models.group_member import GroupMember

def calculate_net_balances(
    group_id: int,
    db: Session
):
    balances = {}

    # Get all group members
    members = (
        db.query(User)
        .join(
            GroupMember,
            User.id == GroupMember.user_id
        )
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    # Initialize balances
    for member in members:
        balances[member.id] = 0

    # Process expenses
    expenses = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    for expense in expenses:

        splits = (
            db.query(ExpenseSplit)
            .filter(
                ExpenseSplit.expense_id == expense.id
            )
            .all()
        )

        for split in splits:

            if split.user_id == expense.paid_by:
                continue

            balances[expense.paid_by] += split.amount
            balances[split.user_id] -= split.amount

    # Process settlements
    settlements = (
        db.query(Settlement)
        .filter(Settlement.group_id == group_id)
        .all()
    )

    for settlement in settlements:

        balances[settlement.payer_id] += settlement.amount
        balances[settlement.receiver_id] -= settlement.amount

    return balances

def get_balances(group_id: int, db: Session):

    balances = {}

    # Process all expenses
    expenses = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    for expense in expenses:

        payer = (
            db.query(User)
            .filter(User.id == expense.paid_by)
            .first()
        )

        splits = (
            db.query(ExpenseSplit)
            .filter(ExpenseSplit.expense_id == expense.id)
            .all()
        )

        for split in splits:

            if split.user_id == expense.paid_by:
                continue

            debtor = (
                db.query(User)
                .filter(User.id == split.user_id)
                .first()
            )

            key = (debtor.email, payer.email)

            balances[key] = balances.get(key, 0) + split.amount

    # Process settlements
    settlements = (
        db.query(Settlement)
        .filter(Settlement.group_id == group_id)
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

        key = (payer.email, receiver.email)

        if key in balances:
            balances[key] -= settlement.amount

    # Build response
    result = []

    for (from_user, to_user), amount in balances.items():

        if amount > 0:

            result.append(
                {
                    "from_user": from_user,
                    "to_user": to_user,
                    "amount": round(amount, 2)
                }
            )

    return result

def get_member_balances(
    group_id: int,
    db: Session
):
    balances = {}

    # Get all group members
    members = (
        db.query(User)
        .join(
            GroupMember,
            User.id == GroupMember.user_id
        )
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    # Initialize every member's balance to 0
    for member in members:
        balances[member.email] = 0

    # Process expenses
    expenses = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    for expense in expenses:

        payer = (
            db.query(User)
            .filter(User.id == expense.paid_by)
            .first()
        )

        splits = (
            db.query(ExpenseSplit)
            .filter(
                ExpenseSplit.expense_id == expense.id
            )
            .all()
        )

        for split in splits:

            if split.user_id == expense.paid_by:
                continue

            debtor = (
                db.query(User)
                .filter(User.id == split.user_id)
                .first()
            )

            balances[payer.email] += split.amount
            balances[debtor.email] -= split.amount

    # Process settlements
    settlements = (
        db.query(Settlement)
        .filter(Settlement.group_id == group_id)
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

        balances[payer.email] += settlement.amount
        balances[receiver.email] -= settlement.amount

    result = []

    for email, balance in balances.items():

        result.append(
            {
                "user": email,
                "net_balance": round(balance, 2)
            }
        )

    return result

def get_simplified_balances(
    group_id: int,
    db: Session
):
    net_balances = calculate_net_balances(
        group_id,
        db
    )

    creditors = []
    debtors = []

    # Separate creditors and debtors
    for user_id, balance in net_balances.items():

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if balance > 0:
            creditors.append(
                {
                    "email": user.email,
                    "amount": round(balance, 2)
                }
            )

        elif balance < 0:
            debtors.append(
                {
                    "email": user.email,
                    "amount": round(abs(balance), 2)
                }
            )

    result = []

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):

        pay_amount = min(
            debtors[i]["amount"],
            creditors[j]["amount"]
        )

        result.append(
            {
                "from_user": debtors[i]["email"],
                "to_user": creditors[j]["email"],
                "amount": round(pay_amount, 2)
            }
        )

        debtors[i]["amount"] -= pay_amount
        creditors[j]["amount"] -= pay_amount

        if debtors[i]["amount"] == 0:
            i += 1

        if creditors[j]["amount"] == 0:
            j += 1

    return result

def get_overall_balance(
    user_id: int,
    db: Session
):
    overall_balance = 0

    # Get all groups the user belongs to
    memberships = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == user_id)
        .all()
    )

    for membership in memberships:

        net_balances = calculate_net_balances(
            membership.group_id,
            db
        )

        overall_balance += net_balances.get(user_id, 0)

    return {
        "user_id": user_id,
        "overall_balance": round(overall_balance, 2)
    }
