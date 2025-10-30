from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, EntityRecord, Investigation

_engine = create_engine("sqlite:///osint.sqlite", echo=False, future=True)
_SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=_engine)


def get_session() -> Session:
    return _SessionLocal()
