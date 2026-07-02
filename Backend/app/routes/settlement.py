from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.schemas.settlement import (
    SettlementCreate,
    SettlementResponse,
    SettlementHistoryResponse
)
from app.services.settlement_service import (
    create_settlement,
    get_settlements
)

router = APIRouter(
    prefix="/settlements",
    tags=["Settlements"]
)


@router.post("/", response_model=SettlementResponse)
def create_new_settlement(
    settlement: SettlementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_settlement(
        settlement=settlement,
        current_user=current_user,
        db=db
    )


@router.get("/{group_id}", response_model=List[SettlementHistoryResponse])
def settlement_history(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_settlements(
        group_id,
        db
    )