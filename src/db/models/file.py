from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

from ...core.utils import generate_time


class File(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )

    user_id: uuid.UUID = Field(
        foreign_key="user.id",
        nullable=False,
        ondelete="CASCADE"
    )

    filename: str = Field(nullable=False)
    filepath: str = Field(nullable=False)
    size_bytes: int = Field(nullable=False, gt=0)
    mime_type: str = Field(nullable=False)

    uploaded_at: datetime = Field(
        default_factory=generate_time,
        nullable=False
    )

    printed: bool = Field(
        nullable=False,
        default=False
    )

