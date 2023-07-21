import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from managers import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for handling client connections.

    Args:
        websocket (WebSocket): The WebSocket instance representing the client connection.

    Returns:
        None
    """
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, timeout_keep_alive=10)
