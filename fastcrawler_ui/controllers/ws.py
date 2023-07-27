import asyncio

from fastapi import Depends, WebSocket, WebSocketDisconnect

from fastcrawler_ui.repository.ws import ConnectionRepository


class WSController:
    def __init__(self, ws_connection_repo: ConnectionRepository = Depends(ConnectionRepository)):
        self.ws_connection_repo = ws_connection_repo

    async def get_connection(self, websocket: WebSocket):
        await self.ws_connection_repo.connect(websocket)
        try:
            while True:
                await asyncio.sleep(1)
        except WebSocketDisconnect:
            self.ws_connection_repo.disconnect(websocket)
