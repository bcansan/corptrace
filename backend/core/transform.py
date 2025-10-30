from __future__ import annotations
from typing import List, Union
from abc import ABC, abstractmethod
from .entity import Entity

class Transform(ABC):
    name: str
    input_type: str
    output_types: List[str]
    description: str
    
    def __init__(self, name: str, input_type: str, output_types: Union[str, List[str]], description: str = "") -> None:
        self.name = name
        self.input_type = input_type
        # Convertir a lista si es string
        if isinstance(output_types, str):
            self.output_types = [output_types]
        else:
            self.output_types = output_types
        self.description = description
    
    @abstractmethod
    async def execute(self, entity: Entity) -> List[Entity]:
        raise NotImplementedError
    
    def to_dict(self):
        return {
            'name': self.name,
            'input_type': self.input_type,
            'output_types': self.output_types,
            'description': self.description
        }