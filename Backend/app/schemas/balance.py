from pydantic import BaseModel


class BalanceResponse(BaseModel):
    from_user: str
    to_user: str
    amount: float
from pydantic import BaseModel


class MemberBalanceResponse(BaseModel):
    user: str
    net_balance: float