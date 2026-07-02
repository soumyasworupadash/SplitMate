from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.current_user import get_current_user
from app.models.user import User

from app.database import get_db
from app.schemas.balance import (
    BalanceResponse,
    MemberBalanceResponse
)
from app.services.balance_service import (
    get_balances,
    get_member_balances,
    get_simplified_balances,
    get_overall_balance
)

router = APIRouter(
    prefix="/balances",
    tags=["Balances"]
)

@router.get("/overall")
def read_overall_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_overall_balance(
        current_user.id,
        db
    )
@router.get("/{group_id}", response_model=List[BalanceResponse])
def read_balances(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_balances(group_id, db)

@router.get(
    "/{group_id}/members",
    response_model=List[MemberBalanceResponse]
)
def read_member_balances(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_member_balances(
        group_id,
        db
    )

@router.get(
    "/{group_id}/simplified",
    response_model=List[BalanceResponse]
)
def read_simplified_balances(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_simplified_balances(
        group_id,
        db
    )

