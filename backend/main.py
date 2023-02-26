import asyncio

from typing import List

from models import Message


from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from kafka import KafkaConsumer


app = FastAPI()
templates = Jinja2Templates(directory="templates")

consumer = KafkaConsumer('ti-monitor')


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Message, client: WebSocket = None):
        if client:
            await client.send_json([message.json()])
        else:
            for connection in self.active_connections:
                await connection.send_json([message.json()])


manager = ConnectionManager()


@app.get("/hello")
def root(request: Request):
    return templates.TemplateResponse("index.htm", {"request": request})


@app.websocket("/api/socket")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        for msg in consumer:
            raw = msg[6].decode().split(';')
            payload = {'id': int(raw[0]), 'timestamp': raw[1], 'altitude': float(raw[2])}
            print(payload)
            await asyncio.sleep(0.01)
            await manager.broadcast(Message(**payload), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
