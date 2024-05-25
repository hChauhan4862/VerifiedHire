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
from db import deta_obj as deta, blockchain, blockChainTransact

# from utils.session import SessionData

class SessionData(BaseModel):
    username: str


class InDetaSHBackend(Generic[ID, SessionModel], SessionBackend[ID, SessionModel]):
    """Stores session data in a dictionary."""

    def __init__(self) -> None:
        """Initialize a new in-memory database."""


    async def create(self, session_id: ID, data: SessionModel):
        """Create a new session entry."""
        pass

    async def read(self, session_id: ID):
        """Read an existing session data."""
        data = blockchain.functions.sessionData(str(session_id)).call()
        if data == "":
            return
        
        return SessionData(username=data)

    async def update(self, session_id: ID, data: SessionModel) -> None:
        """Update an existing session."""
        pass

    async def delete(self, session_id: ID) -> None:
        """D"""
        pass
