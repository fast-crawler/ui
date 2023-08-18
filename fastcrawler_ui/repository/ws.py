from fastapi import WebSocket
from pydantic import BaseModel


class Message(BaseModel):
    """
    Represents a message sent over WebSocket.
    """

    content: str
    sender: str


class ConnectionRepository:
    """
    Manages WebSocket connections for the FastAPI application.
    """

    def __init__(self):
        """
        Initializes the ConnectionRepository.
        """
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """
        Handles the connection of a new WebSocket client.

        Args:
            websocket (WebSocket): The WebSocket instance representing the client connection.

        Returns:
            None
        """
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Handles the disconnection of a WebSocket client.

        Args:
            websocket (WebSocket): The WebSocket instance representing the client connection.

        Returns:
            None
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: Message, websocket: WebSocket):
        """
        Sends a personal message to a specific WebSocket client.

        Args:
            message (Message): The message to send.
            websocket (WebSocket): The WebSocket instance representing the client connection.

        Returns:
            None
        """
        await websocket.send_json(message.model_dump())

    async def broadcast(self, message: Message):
        """
        Broadcasts a message to all connected WebSocket clients.

        Args:
            message (Message): The message to broadcast.

        Returns:
            None
        """
        for connection in self.active_connections:
            await connection.send_json(message.model_dump())
