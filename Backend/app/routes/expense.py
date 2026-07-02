from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.message import MessageResponse
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse
)
from app.services.expense_service import (
    create_expense,
    update_expense,
    delete_expense,
    get_group_expenses
)

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("/", response_model=ExpenseResponse)
def create_new_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_expense(
        expense=expense,
        current_user=current_user,
        db=db
    )

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_existing_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_expense(
        expense_id=expense_id,
        expense=expense,
        current_user=current_user,
        db=db
    )

@router.delete("/{expense_id}", response_model=MessageResponse)
def delete_existing_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_expense(
        expense_id=expense_id,
        current_user=current_user,
        db=db
    )

from typing import List


@router.get("/group/{group_id}", response_model=List[ExpenseResponse])
def read_group_expenses(
    group_id: int,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "amount",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return get_group_expenses(
        group_id=group_id,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
        db=db
    )
