from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal

from app.models.user import User
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_or_create_user(db, name, email, password):
    user = db.query(User).filter(User.email == email).first()

    if user:
        return user

    user = User(
        name=name,
        email=email,
        password=pwd_context.hash(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"Created user: {email}")

    return user


def get_or_create_group(db, name, owner):

    group = (
        db.query(Group)
        .filter(
            Group.name == name,
            Group.owner_id == owner.id
        )
        .first()
    )

    if group:
        return group

    group = Group(
        name=name,
        owner_id=owner.id
    )

    db.add(group)
    db.commit()
    db.refresh(group)

    print(f"Created group: {name}")

    return group


def add_member(db, group, user):

    exists = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group.id,
            GroupMember.user_id == user.id
        )
        .first()
    )

    if not exists:

        db.add(
            GroupMember(
                group_id=group.id,
                user_id=user.id
            )
        )

        db.commit()

        print(f"Added {user.email} to {group.name}")


def create_expense_if_not_exists(
    db,
    description,
    amount,
    payer,
    group,
    splits
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.description == description,
            Expense.group_id == group.id
        )
        .first()
    )

    if expense:
        return

    expense = Expense(
        description=description,
        amount=amount,
        paid_by=payer.id,
        group_id=group.id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    for user, split_amount in splits:

        db.add(
            ExpenseSplit(
                expense_id=expense.id,
                user_id=user.id,
                amount=split_amount
            )
        )

    db.commit()

    print(f"Created expense: {description}")


def seed():

    db: Session = SessionLocal()

    try:

        soumya = get_or_create_user(
            db,
            "Soumya",
            "soumya@gmail.com",
            "password123"
        )

        kalyani = get_or_create_user(
            db,
            "Kalyani",
            "kalyani@gmail.com",
            "password123"
        )

        group = get_or_create_group(
            db,
            "Goa Trip",
            soumya
        )

        add_member(db, group, soumya)
        add_member(db, group, kalyani)

        create_expense_if_not_exists(
            db,
            "Hotel",
            4000,
            soumya,
            group,
            [
                (soumya, 2000),
                (kalyani, 2000),
            ]
        )

        create_expense_if_not_exists(
            db,
            "Taxi",
            1000,
            kalyani,
            group,
            [
                (soumya, 500),
                (kalyani, 500),
            ]
        )

        print("\nSeed completed successfully.")

    finally:

        db.close()


if __name__ == "__main__":
    seed()