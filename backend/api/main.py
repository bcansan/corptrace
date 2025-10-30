import sys
from pathlib import Path

# Ensure backend/ directory is on sys.path when running from backend/
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
	sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.transforms import router as transforms_router
from api.routes.entities import router as entities_router

app = FastAPI(title="CorpTrace OSINT API", version="0.1.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
	return {"status": "ok"}


app.include_router(transforms_router)
app.include_router(entities_router)
