from pydantic import BaseModel, Field


class SettlementCreate(BaseModel):
    group_id: int
    receiver_id: int
    amount: float = Field(..., gt=0)


from datetime import datetime

class SettlementResponse(BaseModel):
    id: int
    group_id: int
    payer_id: int
    receiver_id: int
    amount: float
    settled_at: datetime

    class Config:
        from_attributes = True

class SettlementHistoryResponse(BaseModel):
    payer: str
    receiver: str
    amount: float
    settled_at: datetime