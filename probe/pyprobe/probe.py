#!/usr/bin/env python3
import asyncio
import secrets
from contextlib import asynccontextmanager
from datetime import datetime

import httpx
from bleak import BleakScanner
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel


# state management
class ProbeState:
    def __init__(self):
        self.pairing_mode = True
        self.pairing_code = secrets.randbelow(900000) + 100000
        self.token = None
        self.watchtower_url = None
        self.scanning = False
        self.devices = {}
        self.scan_task = None
        self.report_task = None

state = ProbeState()

# models
class AdoptRequest(BaseModel):
    code: int
    ip: str
    token: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"pairing code: {state.pairing_code}")
    yield
    if state.scan_task:
        state.scan_task.cancel()
    if state.report_task:
        state.report_task.cancel()

app = FastAPI(lifespan=lifespan)

def verify_token(authorization: str = Header(None)):
    if state.pairing_mode:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "probe not adopted")
    if not authorization or authorization != f"Bearer {state.token}":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")

def callback(device, adv_data):
    if adv_data.rssi is None:
        return
    state.devices[device.address] = {
        "rssi": adv_data.rssi,
        "timestamp": datetime.now().isoformat()
    }

async def scan_loop():
    scanner = BleakScanner(detection_callback=callback)
    await scanner.start()
    try:
        while state.scanning:
            await asyncio.sleep(1)
    finally:
        await scanner.stop()

async def report_loop():
    async with httpx.AsyncClient() as client:
        while state.scanning:
            try:
                print(f"sending report to {state.watchtower_url}/report:")
                print(state.devices)
                await client.post(
                    f"{state.watchtower_url}/report",
                    json={"devices": state.devices},
                    headers={"Authorization": f"Bearer {state.token}"}
                )
                state.devices = {}
            except Exception as e:
                print(f"failed to report: {e}")
            await asyncio.sleep(5)

@app.post("/adopt")
async def adopt(req: AdoptRequest):
    if not state.pairing_mode:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "already adopted")
    if req.code != state.pairing_code:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid code")

    state.token = req.token
    state.watchtower_url = f"http://{req.ip}:8001"
    state.pairing_mode = False

    return {"status": "probe adopted"}

@app.post("/scan/start")
async def scan_start(authorization: str = Header(None)):
    verify_token(authorization)
    if state.scanning:
        return {"status": "already scanning"}

    state.scanning = True
    state.scan_task = asyncio.create_task(scan_loop())
    state.report_task = asyncio.create_task(report_loop())

    return {"status": "probe has started scanning"}

@app.post("/scan/stop")
async def scan_stop(authorization: str = Header(None)):
    verify_token(authorization)
    if not state.scanning:
        return {"status": "not scanning"}

    state.scanning = False
    if state.scan_task:
        state.scan_task.cancel()
    if state.report_task:
        state.report_task.cancel()

    return {"status": "probe has stopped scanning"}
