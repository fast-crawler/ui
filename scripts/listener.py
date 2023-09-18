import asyncio
import json

import websockets


async def listener():
    uri = "ws://localhost:8001/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            message_obj = json.loads(message)
            print(f"Received message from {message_obj['sender']}: {message_obj['content']}")


if __name__ == "__main__":
    asyncio.run(listener())
