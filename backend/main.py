import asyncio

from tools import csv_to_df

import json
from asyncio import sleep

from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates

from kafka import KafkaConsumer

app = FastAPI()
templates = Jinja2Templates(directory="templates")

consumer = KafkaConsumer('ti-monitor')

# for msg in consumer:
#     raw = msg[6].decode().split(';')
#     payload = {'time': raw[0], 'altitude': raw[1]}
#     print(payload)


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.htm", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    for msg in consumer:
        raw = msg[6].decode().split(';')
        payload = {'time': raw[0], 'altitude': raw[1]}
        print(payload)
        await asyncio.sleep(0.1)
        await websocket.send_json(payload)