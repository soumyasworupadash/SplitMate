from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class SplitDetail(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0)


class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=2, max_length=255)
    amount: float = Field(..., gt=0)
    group_id: int

    # New fields
    split_type: Literal["equal", "exact"] = "equal"
    splits: Optional[List[SplitDetail]] = None

class ExpenseUpdate(BaseModel):
    description: str = Field(..., min_length=2, max_length=255)
    amount: float = Field(..., gt=0)

    split_type: Literal["equal", "exact"] = "equal"
    splits: Optional[List[SplitDetail]] = None


class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    paid_by:int
    paid_by_name: str
    group_id: int

    class Config:
        from_attributes = True