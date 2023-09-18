import asyncio
import json

import websockets


async def sender():
    uri = "ws://localhost:8001/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            content = input("Enter your message content: ")
            sender_name = input("Enter your name: ")
            message = json.dumps({"content": content, "sender": sender_name})
            await websocket.send(message)


if __name__ == "__main__":
    asyncio.run(sender())
