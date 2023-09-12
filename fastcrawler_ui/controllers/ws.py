import json

from fastapi import Depends, WebSocket

from fastcrawler_ui.repository.ws import ConnectionRepository, Message


class WSController:
    def __init__(self, ws_connection_repo: ConnectionRepository = Depends(ConnectionRepository)):
        self.ws_connection_repo = ws_connection_repo

    async def get_and_send_message(self, websocket: WebSocket):
        async with self.ws_connection_repo.open_connection(websocket) as connection:
            while True:
                print("HEY!")
                data = await websocket.receive_text()
                data_obj = Message.model_construct(**json.loads(data))
                connection.messages.append(data_obj)
                await connection.broadcast(exclude_connection={websocket})
