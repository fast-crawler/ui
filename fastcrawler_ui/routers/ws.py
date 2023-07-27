from fastapi import APIRouter, Depends, WebSocket

from fastcrawler_ui.controllers.ws import WSController

router = APIRouter()


@router.websocket("/ws")
async def clients(
    websocket: WebSocket,
    ws_controller: WSController = Depends(WSController),
):
    """
    WebSocket endpoint for handling client connections.

    Args:
        websocket (WebSocket): The WebSocket instance representing the client connection.

    Returns:
        None
    """
    await ws_controller.get_connection(websocket)
