import asyncio

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from fastcrawler_ui.controllers.ws import ConnectionManager

router = APIRouter()


@router.websocket("/ws")
async def clients(
    websocket: WebSocket,
    connection: ConnectionManager = Depends(ConnectionManager),
):
    """
    WebSocket endpoint for handling client connections.

    Args:
        websocket (WebSocket): The WebSocket instance representing the client connection.

    Returns:
        None
    """
    await connection.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        connection.disconnect(websocket)
