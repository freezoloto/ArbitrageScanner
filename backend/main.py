from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import threading
import json
import asyncio

from scanner import scanner_loop
from scanner_state import scanner_state

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Фронтенд отдаём по /app
app.mount("/app", StaticFiles(directory="F:/Scanner/frontend", html=True), name="frontend")


# === WebSocket менеджер ===
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message):
        dead = []
        for ws in self.active_connections:
            try:
                await ws.send_text(json.dumps(message))
            except:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


# === Запуск сканера в отдельном потоке ===
def start_scanner():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def on_update_async(opps):
        await manager.broadcast({"type": "update", "data": opps})

    def on_update(opps):
        asyncio.run_coroutine_threadsafe(on_update_async(opps), loop)

    def run():
        scanner_loop(on_update)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    loop.run_forever()


@app.on_event("startup")
def startup_event():
    t = threading.Thread(target=start_scanner, daemon=True)
    t.start()


# === API ===

@app.get("/api/opps")
def get_opps():
    return scanner_state.get_results()


@app.post("/api/settings/min_spread")
def set_min_spread(value: float):
    scanner_state.set_min_spread(value)
    return {"status": "ok"}


@app.post("/api/settings/fee_mode")
def set_fee_mode(mode: str):
    scanner_state.set_fee_mode(mode)
    return {"status": "ok"}


@app.post("/api/settings/exchanges")
def set_exchanges(lst: list = Body(...)):
    scanner_state.set_enabled_exchanges(lst)
    return {"status": "ok"}


@app.post("/api/settings/pairs")
def set_pairs(lst: list = Body(...)):
    scanner_state.set_enabled_pairs(lst)
    return {"status": "ok"}


@app.post("/api/settings/sort")
def set_sort(field: str, desc: bool):
    scanner_state.set_sort(field, desc)
    return {"status": "ok"}


# === WebSocket ===
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        await ws.send_text(json.dumps({
            "type": "update",
            "data": scanner_state.get_results()
        }))
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(ws)
