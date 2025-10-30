from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..database.queries import init_db
from .routes.entities import router as entities_router
from .routes.transforms import router as transforms_router

app = FastAPI(title="Corporate OSINT API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(entities_router)
app.include_router(transforms_router)
