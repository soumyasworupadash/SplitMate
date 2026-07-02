import asyncio

from app.services.websocket_manager import manager


def broadcast_group_update(
    group_id: int,
    event: str
):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(
            manager.broadcast(
                group_id,
                {
                    "event": event,
                    "group_id": group_id
                }
            )
        )
    except RuntimeError:
        pass