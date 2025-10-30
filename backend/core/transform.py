from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from .entity import Entity


class Transform(ABC):
    name: str
    input_type: str
    output_type: str

    def __init__(self, name: str, input_type: str, output_type: str) -> None:
        self.name = name
        self.input_type = input_type
        self.output_type = output_type

    @abstractmethod
    async def execute(self, entity: Entity) -> List[Entity]:
        raise NotImplementedError
