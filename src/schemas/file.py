from pydantic import BaseModel
from datetime import datetime
import uuid


class FileCreate(BaseModel):
    filename: str
    filepath: str
    size_bytes: int
    mime_type: str


class FileRead(BaseModel):
    id: uuid.UUID
    filename: str
    size_bytes: int
    mime_type: str
    uploaded_at: datetime
