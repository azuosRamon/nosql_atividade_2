from __future__ import annotations
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def iso(dt: datetime) -> str:
    """
    Converte datetime para string ISO 8601 com timezone UTC.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def serialize(doc: dict) -> dict:
    """
    Serializa um documento MongoDB para dict serializável em JSON.
    Converte ObjectId e datetime.
    """
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    if "created_at" in d and isinstance(d["created_at"], datetime):
        d["created_at"] = iso(d["created_at"])
    return d

class MessageIn(BaseModel):
    """
    Modelo de entrada de mensagem.
    """
    username: str = Field(..., max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)

class MessageOut(BaseModel):
    """
    Modelo de saída de mensagem.
    """
    _id: str
    room: str
    username: str
    content: str
    created_at: str