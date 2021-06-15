import asyncio
import websockets
import json


async def send_mess():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        user_mess = json.dumps({"name": "user12", "message": "Some text - 12"})
        await websocket.send(user_mess)
        result = await websocket.recv()


asyncio.get_event_loop().run_until_complete(send_mess())
