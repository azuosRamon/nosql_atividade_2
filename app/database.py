from __future__ import annotations
import os
from typing import Optional

from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path

# carrega .env
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=ROOT / ".env")

MONGO_URL = os.getenv("MONGO_URL", "")
MONGO_DB = os.getenv("MONGO_DB", "chatdb")

# --- DB helpers ---
_client: Optional[AsyncIOMotorClient] = None


def db():
    global _client
    if _client is None:
        if not MONGO_URL:
            raise RuntimeError("Defina MONGO_URL no .env (string do MongoDB Atlas).")
        _client = AsyncIOMotorClient(MONGO_URL)
    return _client[MONGO_DB]
