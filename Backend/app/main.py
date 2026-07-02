from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.routes.group import router as group_router
from app.routes import expense
from app.routes import history
from app.routes import balance
from app.models.activity_log import Activity
from app.routes import settlement
from app.routes import websocket
from app.routes import dashboard
from app.routes import activity
app = FastAPI(
    title="SplitMate API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(group_router)
app.include_router(expense.router)
app.include_router(balance.router)
app.include_router(settlement.router)
app.include_router(history.router)
app.include_router(activity.router)
app.include_router(websocket.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {
        "message": "SplitMate Backend Running"
    }


@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }