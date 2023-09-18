import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Self

from fastapi import WebSocket
from pydantic import BaseModel


class Message(BaseModel):
    """
    Represents a message sent over WebSocket.
    """

    content: str
    sender: str


class ConnectionRepository:
    active_connections: set[WebSocket] = set()
    messages: list[Message] = []

    """
    Manages WebSocket connections for the FastAPI application.
    """

    @asynccontextmanager
    async def open_connection(self, websocket: WebSocket) -> AsyncGenerator[Self, None]:
        """
        Context manager to manage WebSocket connections.

        Args:
            websocket (WebSocket): The WebSocket instance representing the client connection.

        Yields:
            None
        """
        await self.connect(websocket)

        try:
            while True:
                yield self
        finally:
            self.disconnect(websocket)

    async def connect(self, websocket: WebSocket):
        """
        Handles the connection of a new WebSocket client.

        Args:
            websocket (WebSocket): The WebSocket instance representing the client connection.

        Returns:
            None
        """
        await websocket.accept()
        ConnectionRepository.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Handles the disconnection of a WebSocket client.

        Args:
            websocket (WebSocket): The WebSocket instance representing the client connection.

        Returns:
            None
        """
        ConnectionRepository.active_connections.remove(websocket)

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

    async def broadcast(self, exclude_connection: set[WebSocket] | None = None):
        """
        Broadcasts a message to all connected WebSocket clients.

        Args:
            message (Message): The message to broadcast.

        Returns:
            None
        """

        await asyncio.gather(
            *[
                connection.send_json(message.model_dump())
                for message in ConnectionRepository.messages
                for connection in ConnectionRepository.active_connections
                if not exclude_connection or connection not in exclude_connection
            ]
        )
        ConnectionRepository.messages = []
