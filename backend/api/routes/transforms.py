from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.transforms.registry import transform_registry
from backend.core.entity import Entity

router = APIRouter()


class TransformRequest(BaseModel):
	entity: dict
	transform_name: str


@router.get("/transforms")
async def list_transforms():
	"""
	Lista todas las transformaciones disponibles
	"""
	return {"transforms": transform_registry.list_all()}


@router.get("/transforms/entity/{entity_type}")
async def get_transforms_for_entity(entity_type: str):
	"""
	Obtiene transformaciones disponibles para un tipo de entidad
	"""
	transforms = transform_registry.get_transforms_for_entity(entity_type)
	return {
		"entity_type": entity_type,
		"available_transforms": [
			{
				'name': t.name,
				'output_types': t.output_types,
				'description': t.description
			}
			for t in transforms
		]
	}


@router.post("/transforms/execute")
async def execute_transform(request: TransformRequest):
	"""
	Ejecuta una transformación sobre una entidad
	"""
	entity = Entity(
		entity_type=request.entity['type'],
		properties=request.entity['properties']
	)
	transform = transform_registry.get_transform(request.transform_name)
	if not transform:
		raise HTTPException(status_code=404, detail="Transform not found")
	try:
		results = await transform.execute(entity)
		return {
			"input_entity": request.entity,
			"transform": request.transform_name,
			"results": [r.to_dict() for r in results],
			"count": len(results)
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
