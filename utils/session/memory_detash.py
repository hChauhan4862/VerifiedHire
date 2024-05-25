"""InMemoryBackend implementation."""
from typing import Dict, Generic
from pydantic import BaseModel
import json

from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel
)
from fastapi_sessions.frontends.session_frontend import ID
from db import deta_obj as deta

# from utils.session import SessionData

class SessionData(BaseModel):
    username: str


class InDetaSHBackend(Generic[ID, SessionModel], SessionBackend[ID, SessionModel]):
    """Stores session data in a dictionary."""

    def __init__(self) -> None:
        """Initialize a new in-memory database."""


    async def create(self, session_id: ID, data: SessionModel):
        """Create a new session entry."""
        if deta.db.sessions.get(str(session_id)):
            raise BackendError("create can't overwrite an existing session")

        deta.db.sessions.put({
            "session_data" : data.model_dump_json()
        }, key=str(session_id))

    async def read(self, session_id: ID):
        """Read an existing session data."""
        data = deta.db.sessions.get(str(session_id))
        if not data:
            return
        
        return SessionData(username=json.loads(data["session_data"])["username"] )

    async def update(self, session_id: ID, data: SessionModel) -> None:
        """Update an existing session."""
        if deta.db.sessions.get(session_id):
             deta.db.sessions.put({
                "session_data" : data.copy(deep=True)
            }, key=str(session_id))
        else:
            raise BackendError("session does not exist, cannot update")

    async def delete(self, session_id: ID) -> None:
        """D"""
        deta.db.sessions.delete(str(session_id))
