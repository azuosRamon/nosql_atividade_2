from __future__ import annotations
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Body, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime, timezone

from app.database import db
from app.ws_manager import manager
from app.models import serialize, MessageIn, MessageOut

router = APIRouter()

# --- REST ---
@router.get("/rooms/{room}/messages", response_model=dict)
async def get_messages(
    room: str, limit: int = Query(20, ge=1, le=100), before_id: str | None = Query(None)
):
    query = {"room": room}
    if before_id:
        try:
            query["_id"] = {"$lt": ObjectId(before_id)}
        except Exception:
            raise HTTPException(status_code=400, detail="before_id inválido")

    cursor = db()["messages"].find(query).sort("_id", -1).limit(limit)
    docs = [serialize(d) async for d in cursor]
    docs.reverse()
    next_cursor = docs[0]["_id"] if docs else None
    return {"items": docs, "next_cursor": next_cursor}

@router.post("/rooms/{room}/messages", status_code=201, response_model=MessageOut)
async def post_message(
    room: str,
    message: MessageIn
):
    if not message.content.strip():
        raise HTTPException(status_code=400, detail="Conteúdo da mensagem não pode ser vazio.")
    doc = {
        "room": room,
        "username": message.username[:50],
        "content": message.content[:1000],
        "created_at": datetime.now(timezone.utc),
    }
    res = await db()["messages"].insert_one(doc)
    doc["_id"] = res.inserted_id
    return serialize(doc)

# --- WS ---
@router.websocket("/ws/{room}")
async def ws_room(ws: WebSocket, room: str):
    await manager.connect(room, ws)
    try:
        # histórico inicial
        cursor = db()["messages"].find({"room": room}).sort("_id", -1).limit(20)
        items = [serialize(d) async for d in cursor]
        items.reverse()
        await ws.send_json({"type": "history", "items": items})

        while True:
            payload = await ws.receive_json()
            try:
                message = MessageIn(**payload)
            except Exception as e:
                await ws.send_json({"type": "error", "detail": "Dados inválidos."})
                continue
            if not message.content.strip():
                await ws.send_json({"type": "error", "detail": "Conteúdo da mensagem não pode ser vazio."})
                continue
            doc = {
                "room": room,
                "username": message.username[:50],
                "content": message.content[:1000],
                "created_at": datetime.now(timezone.utc),
            }
            res = await db()["messages"].insert_one(doc)
            doc["_id"] = res.inserted_id
            await manager.broadcast(room, {"type": "message", "item": serialize(doc)})
    except WebSocketDisconnect:
        manager.disconnect(room, ws)