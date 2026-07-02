from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(
        self,
        group_id: int,
        websocket: WebSocket
    ):
        await websocket.accept()
        self.active_connections[group_id].append(websocket)

    def disconnect(
        self,
        group_id: int,
        websocket: WebSocket
    ):
        if websocket in self.active_connections[group_id]:
            self.active_connections[group_id].remove(websocket)

    async def broadcast(
        self,
        group_id: int,
        message: dict
    ):
        disconnected = []

        for connection in self.active_connections[group_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.active_connections[group_id].remove(connection)


manager = ConnectionManager()