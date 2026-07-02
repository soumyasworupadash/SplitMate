from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import create_user
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import login_user
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(user, db)

    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return new_user
@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    token = login_user(
        credentials.email,
        credentials.password,
        db
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return token