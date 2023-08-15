import asyncio
from unittest.mock import AsyncMock

import pytest
from fastapi import WebSocket
from fastcrawler_ui.repository.ws import ConnectionRepository, Message

from tests.conftest import client, websocket


async def override_get_connection__send_data(self, websocket: WebSocket):
    await self.ws_connection_repo.connect(websocket)
    await websocket.accept()
    await websocket.send_json({"test": "OK"})
    self.ws_connection_repo.disconnect(websocket)


async def override_get_connection__receive_data(self, websocket: WebSocket):
    await self.ws_connection_repo.connect(websocket)
    await websocket.accept()
    res = await websocket.receive_json()
    self.ws_connection_repo.disconnect(websocket)
    return res


@pytest.mark.asyncio
async def test_websocket_connect(manager: ConnectionRepository, websocket):
    await manager.connect(websocket)
    assert websocket in manager.active_connections


@pytest.mark.asyncio
async def test_connection_manager_broadcast(manager: ConnectionRepository):
    websocket_mock1 = AsyncMock()
    websocket_mock2 = AsyncMock()

    manager.active_connections.add(websocket_mock1)
    manager.active_connections.add(websocket_mock2)

    message_dict = {"content": "Hello", "sender": "Sadegh"}
    message = Message(**message_dict)

    await manager.broadcast(message)

    websocket_mock1.send_json.assert_called_once_with(message.model_dump())
    websocket_mock2.send_json.assert_called_once_with(message.model_dump())


@pytest.mark.asyncio
async def test_connection_manager_send_personal_message(manager: ConnectionRepository):
    websocket_mock = AsyncMock()

    message_dict = {"content": "Hello", "sender": "Test"}
    message = Message(**message_dict)

    await manager.send_personal_message(message, websocket_mock)

    websocket_mock.send_json.assert_called_once_with(message.model_dump())


@pytest.mark.asyncio
async def test_disconnects(manager: ConnectionRepository):
    websocket = AsyncMock()
    websocket2 = AsyncMock()
    websocket3 = AsyncMock()
    await manager.connect(websocket)
    await manager.connect(websocket2)
    await manager.connect(websocket3)
    # I use the shallow_copy here because RuntimeError: Set changed size during iteration
    active_connections_copy = manager.active_connections.copy()
    for websocket in active_connections_copy:  # type: ignore
        manager.disconnect(websocket)

    assert not manager.active_connections
