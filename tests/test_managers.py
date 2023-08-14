import sys
import os
import asyncio
from unittest.mock import AsyncMock

import pytest
from tests.conftest import client


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastcrawler_ui.repository.ws import ConnectionRepository, Message




def test_websocket_connect(manager: ConnectionRepository, websocket):
    asyncio.run(manager.connect(websocket))
    assert websocket in manager.active_connections


def test_connection_manager_broadcast(manager: ConnectionRepository):
    websocket_mock1 = AsyncMock()
    websocket_mock2 = AsyncMock()

    manager.active_connections.add(websocket_mock1)
    manager.active_connections.add(websocket_mock2)

    message_dict = {"content": "Hello", "sender": "Sadegh"}
    message = Message(**message_dict)

    asyncio.run(manager.broadcast(message))

    websocket_mock1.send_json.assert_called_once_with(message.model_dump())
    websocket_mock2.send_json.assert_called_once_with(message.model_dump())


def test_connection_manager_send_personal_message(manager: ConnectionRepository):
    websocket_mock = AsyncMock()

    message_dict = {"content": "Hello", "sender": "Test"}
    message = Message(**message_dict)

    asyncio.run(manager.send_personal_message(message, websocket_mock))

    websocket_mock.send_json.assert_called_once_with(message.model_dump())


def test_disconnects(manager: ConnectionRepository):
    websocket = AsyncMock()
    websocket2 = AsyncMock()
    websocket3 = AsyncMock()
    asyncio.run(manager.connect(websocket))
    asyncio.run(manager.connect(websocket2))
    asyncio.run(manager.connect(websocket3))
    # I use the shallow_copy here because RuntimeError: Set changed size during iteration
    active_connections_copy = manager.active_connections.copy()
    for websocket in active_connections_copy:  # type: ignore
        manager.disconnect(websocket)

    assert not manager.active_connections
