from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class GroupResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class AddMemberRequest(BaseModel):
    email: str


class GroupMemberResponse(BaseModel):
    id: int
    user_id: int
    group_id: int

    class Config:
        from_attributes = True