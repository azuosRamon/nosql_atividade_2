from __future__ import annotations
from typing import Optional

from app.config import MONGO_URL, MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient

# --- DB helpers ---
_client: Optional[AsyncIOMotorClient] = None

def db():
    """Retorna a instância do banco de dados MongoDB.
    Lança RuntimeError se MONGO_URL não estiver definido."""
    global _client
    if _client is None:
        if not MONGO_URL:
            raise RuntimeError("Defina MONGO_URL no .env (string do MongoDB Atlas).")
        _client = AsyncIOMotorClient(MONGO_URL)
    return _client[MONGO_DB]
