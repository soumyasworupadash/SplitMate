from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_owe: float
    total_owed: float
    net_balance: float
    group_count: int
    highest_owed_group: str | None