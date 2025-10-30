import sys
from pathlib import Path

# Ensure backend/ directory is on sys.path
BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
	sys.path.insert(0, str(BACKEND_DIR))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from uuid import uuid4
import json

# If you later add persistence, wire your DB imports here
# from database.queries import get_session
# from database.models import EntityRecord

router = APIRouter(prefix="/api/entities", tags=["entities"])


class EntityIn(BaseModel):
	type: str
	properties: Dict[str, Any]


@router.post("")
async def create_entity(payload: EntityIn) -> Dict[str, Any]:
	# Placeholder in-memory response (DB wiring can be restored when ready)
	entity_id = str(uuid4())
	return {"id": entity_id, "type": payload.type, "properties": payload.properties}


@router.get("/{entity_id}")
async def get_entity(entity_id: str) -> Dict[str, Any]:
	# Placeholder not found (restore DB lookups when ready)
	raise HTTPException(status_code=404, detail="Entity not found")
