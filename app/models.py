from __future__ import annotations
from datetime import datetime, timezone

def iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def serialize(doc: dict) -> dict:
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    if "created_at" in d and isinstance(d["created_at"], datetime):
        d["created_at"] = iso(d["created_at"])
    return d
