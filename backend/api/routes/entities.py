from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from uuid import uuid4
import json
from ...database.queries import get_session
from ...database.models import EntityRecord

router = APIRouter(prefix="/api/entities", tags=["entities"])


class EntityIn(BaseModel):
    type: str
    properties: Dict[str, Any]


@router.post("")
def create_entity(payload: EntityIn) -> Dict[str, Any]:
    session = get_session()
    try:
        entity_id = str(uuid4())
        rec = EntityRecord(
            id=entity_id,
            type=payload.type,
            properties_json=json.dumps(payload.properties),
            metadata_json=json.dumps({}),
        )
        session.add(rec)
        session.commit()
        return {"id": entity_id, "type": payload.type, "properties": payload.properties}
    finally:
        session.close()


@router.get("/{entity_id}")
def get_entity(entity_id: str) -> Dict[str, Any]:
    session = get_session()
    try:
        rec = session.get(EntityRecord, entity_id)
        if not rec:
            raise HTTPException(status_code=404, detail="Entity not found")
        return {
            "id": rec.id,
            "type": rec.type,
            "properties": json.loads(rec.properties_json),
            "metadata": json.loads(rec.metadata_json or "{}"),
        }
    finally:
        session.close()
