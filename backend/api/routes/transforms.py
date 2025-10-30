from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/api/transforms", tags=["transforms"])


AVAILABLE: List[Dict[str, str]] = [
    {"name": "Company→Domains", "input_type": "Company", "output_type": "Domain"},
    {"name": "Domain→Subdomains", "input_type": "Domain", "output_type": "Domain"},
    {"name": "Domain→IPs", "input_type": "Domain", "output_type": "IPAddress"},
    {"name": "Company→LinkedIn", "input_type": "Company", "output_type": "SocialMediaProfile"},
    {"name": "Domain→Technologies", "input_type": "Domain", "output_type": "Technology"},
]


@router.get("/available")
def list_transforms() -> List[Dict[str, str]]:
    return AVAILABLE


class ExecuteIn(BaseModel):
    transform_name: str
    entity: Dict[str, Any]


@router.post("/execute")
def execute_transform(payload: ExecuteIn) -> Dict[str, Any]:
    # Stub: return empty results for now
    names = [t["name"] for t in AVAILABLE]
    if payload.transform_name not in names:
        raise HTTPException(status_code=400, detail="Unknown transform")
    return {"results": []}
