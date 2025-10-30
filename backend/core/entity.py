from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


@dataclass
class Entity:
    entity_type: str
    properties: Dict[str, Any]
    id: str = field(default_factory=generate_uuid)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def add_property(self, key: str, value: Any) -> None:
        self.properties[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.entity_type,
            "properties": self.properties,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
