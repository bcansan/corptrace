from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class EntityRecord(Base):
    __tablename__ = "entities"

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)
    properties_json = Column(Text, nullable=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    investigation_id = Column(String, ForeignKey("investigations.id"), nullable=True)

    investigation = relationship("Investigation")
