from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User

from app.services.live_update_service import broadcast_group_update
from app.services.activity_service import log_activity
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense_split import ExpenseSplit
def create_expense(
    expense: ExpenseCreate,
    current_user: User,
    db: Session
):
    # Check if group exists
    group = (
        db.query(Group)
        .filter(Group.id == expense.group_id)
        .first()
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found."
        )

    # Check if current user belongs to the group
    member = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == expense.group_id,
            GroupMember.user_id == current_user.id
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this group."
        )

    new_expense = Expense(
        description=expense.description,
        amount=expense.amount,
        paid_by=current_user.id,
        group_id=expense.group_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    members = (
    db.query(GroupMember)
    .filter(GroupMember.group_id == expense.group_id)
    .all()
    )
    # Calculate equal share
    # Equal Split
    if expense.split_type == "equal":

        member_count = len(members)

        base_share = round(expense.amount / member_count, 2)

        shares = [base_share] * member_count

        difference = round(
            expense.amount - sum(shares),
            2
        )

        shares[-1] = round(shares[-1] + difference, 2)

        for member, share in zip(members, shares):

            split = ExpenseSplit(
                expense_id=new_expense.id,
                user_id=member.user_id,
                amount=round(share, 2)
            )

            db.add(split)

        db.commit()


# Exact Split
    elif expense.split_type == "exact":

        # Splits must be provided
        if expense.splits is None or len(expense.splits) == 0:
            raise HTTPException(
                status_code=400,
                detail="Splits are required for exact split."
            )
        
        # Total of all split amounts
        total = sum(split.amount for split in expense.splits)

        if round(total, 2) != round(expense.amount, 2):
            raise HTTPException(
                status_code=400,
                detail="Sum of split amounts must equal the expense amount."
            )
        
        # Validate every user belongs to the group
        for split in expense.splits:

            member = (
                db.query(GroupMember)
                .filter(
                    GroupMember.group_id == expense.group_id,
                    GroupMember.user_id == split.user_id
                )
                .first()
            )

            if member is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"User {split.user_id} is not a member of the group."
                )
        for split in expense.splits:

            expense_split = ExpenseSplit(
                expense_id=new_expense.id,
                user_id=split.user_id,
                amount=split.amount
            )

            db.add(expense_split)

        db.commit()
    log_activity(
        group_id=new_expense.group_id,
        user_id=current_user.id,
        action="Expense Added",
        description=f"{current_user.email} added '{new_expense.description}' (₹{new_expense.amount}).",
        db=db
    )
    broadcast_group_update(
    new_expense.group_id,
    "expense_added"
)


    return new_expense

def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: User,
    db: Session
):
    # Find expense
    existing_expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )

    if existing_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found."
        )

    # Only expense creator can edit (we'll extend this to group owner in Requirement 19)
    group = (
        db.query(Group)
        .filter(Group.id == existing_expense.group_id)
        .first()
    )

    if (
        existing_expense.paid_by != current_user.id
        and group.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the expense creator or group owner can edit this expense."
        )
      
    # Update expense
    existing_expense.description = expense.description
    existing_expense.amount = expense.amount

    db.commit()
    db.refresh(existing_expense)

    # Remove old splits
    (
        db.query(ExpenseSplit)
        .filter(ExpenseSplit.expense_id == expense_id)
        .delete()
    )
    db.commit()

    members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == existing_expense.group_id)
        .all()
    )

    if expense.split_type == "equal":

        member_count = len(members)

        base_share = round(expense.amount / member_count, 2)

        shares = [base_share] * member_count

        difference = round(
            expense.amount - sum(shares),
            2
        )

        shares[-1] = round(shares[-1] + difference, 2)

        for member, share in zip(members, shares):

            db.add(
                ExpenseSplit(
                    expense_id=expense_id,
                    user_id=member.user_id,
                    amount=round(share, 2)
                )
            )

    elif expense.split_type == "exact":

        if expense.splits is None or len(expense.splits) == 0:
            raise HTTPException(
                status_code=400,
                detail="Splits are required for exact split."
            )

        total = sum(split.amount for split in expense.splits)

        if round(total, 2) != round(expense.amount, 2):
            raise HTTPException(
                status_code=400,
                detail="Sum of split amounts must equal the expense amount."
            )

        for split in expense.splits:

            member = (
                db.query(GroupMember)
                .filter(
                    GroupMember.group_id == existing_expense.group_id,
                    GroupMember.user_id == split.user_id
                )
                .first()
            )

            if member is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"User {split.user_id} is not a member of the group."
                )

            db.add(
                ExpenseSplit(
                    expense_id=expense_id,
                    user_id=split.user_id,
                    amount=split.amount
                )
            )

    db.commit()
    log_activity(
        group_id=existing_expense.group_id,
        user_id=current_user.id,
        action="Expense Edited",
        description=f"{current_user.email} edited '{existing_expense.description}'.",
        db=db
    )
    return existing_expense

def delete_expense(
    expense_id: int,
    current_user: User,
    db: Session
):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found."
        )

    # expense creator and group owner can delete
    
    group = (
        db.query(Group)
        .filter(Group.id == expense.group_id)
        .first()
    )

    if (
        expense.paid_by != current_user.id
        and group.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the expense creator or group owner can delete this expense."
        )

    # Delete all expense splits
    (
        db.query(ExpenseSplit)
        .filter(ExpenseSplit.expense_id == expense_id)
        .delete()
    )
    log_activity(
        group_id=expense.group_id,
        user_id=current_user.id,
        action="Expense Deleted",
        description=f"{current_user.email} deleted '{expense.description}'.",
        db=db
    )
    # Delete expense
    db.delete(expense)

    db.commit()

    return {
        "message": "Expense deleted successfully."
    }

def get_group_expenses(
    group_id: int,
    page: int,
    limit: int,
    sort_by: str,
    order: str,
    db: Session
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be at least 1."
        )

    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Limit must be at least 1."
        )

    query = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
    )

# Sorting
    if sort_by == "amount":

        if order == "desc":
            query = query.order_by(Expense.amount.desc())
        else:
         query = query.order_by(Expense.amount.asc())

    elif sort_by == "date":

        if order == "desc":
            query = query.order_by(Expense.created_at.desc())
        else:
            query = query.order_by(Expense.created_at.asc())

    expenses = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    result = []

    for expense in expenses:

        payer = (
            db.query(User)
            .filter(User.id == expense.paid_by)
            .first()
        )

        result.append({
            "id": expense.id,
            "description": expense.description,
            "amount": expense.amount,
            "paid_by": expense.paid_by,
            "paid_by_name": payer.email if payer else "Unknown",
            "group_id": expense.group_id,
        })

    return result
