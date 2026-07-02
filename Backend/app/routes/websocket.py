from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_manager import manager

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"]
)


@router.websocket("/{group_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    group_id: int
):
    await manager.connect(group_id, websocket)

    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(group_id, websocket)