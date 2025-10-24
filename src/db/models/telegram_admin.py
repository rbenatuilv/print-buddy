from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

from ...core.utils import generate_time


class TelegramAdmin(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )

    user_id: uuid.UUID = Field(
        foreign_key="user.id",
        ondelete="CASCADE"
    )

    telegram_id: str = Field(
        nullable=False
    )

    created_at: datetime = Field(
        nullable=False,
        default_factory=generate_time
    )
