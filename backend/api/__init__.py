from .main import app  # noqa: F401
from fastapi import APIRouter
from .routes.entities import router as entities_router
from .routes.transforms import router as transforms_router

# Routers will be included by importing this module in main
app.include_router(entities_router)
app.include_router(transforms_router)
