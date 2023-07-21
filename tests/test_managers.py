import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from managers import ConnectionManager, Message
from main import app


class WebSocketTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.manager = ConnectionManager()
        self.websocket = AsyncMock()

    def test_websocket_connect(self):
        asyncio.run(self.manager.connect(self.websocket))
        self.assertIn(self.websocket, self.manager.active_connections)

    def test_connection_manager_broadcast(self):
        websocket_mock1 = AsyncMock()
        websocket_mock2 = AsyncMock()

        self.manager.active_connections.add(websocket_mock1)
        self.manager.active_connections.add(websocket_mock2)

        message_dict = {"content": "Hello", "sender": "Sadegh"}
        message = Message(**message_dict)

        asyncio.run(self.manager.broadcast(message))

        websocket_mock1.send_json.assert_called_once_with(message.model_dump())
        websocket_mock2.send_json.assert_called_once_with(message.model_dump())

    def test_connection_manager_send_personal_message(self):
        websocket_mock = AsyncMock()

        message_dict = {"content": "Hello", "sender": "Test"}
        message = Message(**message_dict)

        asyncio.run(self.manager.send_personal_message(
            message, websocket_mock))

        websocket_mock.send_json.assert_called_once_with(message.model_dump())

    def test_dissconnects(self):
        websocket = AsyncMock()
        websocket2 = AsyncMock()
        websocket3 = AsyncMock()
        asyncio.run(self.manager.connect(websocket))
        asyncio.run(self.manager.connect(websocket2))
        asyncio.run(self.manager.connect(websocket3))
        # I use the shollow_copy here becuase RuntimeError: Set changed size during iteration
        shollow_copy = self.manager.active_connections.copy()
        for websocket in shollow_copy:
            self.manager.disconnect(websocket)

        self.assertFalse(self.manager.active_connections)


if __name__ == "__main__":
    unittest.main()
