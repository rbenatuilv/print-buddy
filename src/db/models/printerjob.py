from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime
import uuid

from ...core.utils import generate_time


class JobStatus(str, Enum):
    PENDING = "pending"
    HELD = "held"
    PRINTING = "printing"
    STOPPED = "stopped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ABORTED = "aborted"


TRANSIT_STATUS = [
    JobStatus.PENDING,
    JobStatus.HELD,
    JobStatus.PRINTING,
    JobStatus.STOPPED
]


class PrintJob(SQLModel, table=True):

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    cups_id: str = Field(nullable=False, unique=True)

    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")

    printer_id: uuid.UUID = Field(foreign_key="printer.id", ondelete="CASCADE")

    printer_name: str = Field(nullable=False)

    file_id: uuid.UUID = Field(foreign_key="file.id", ondelete="SET NULL", nullable=True)

    file_name: str = Field(nullable=True)

    file_size: int = Field(nullable=True)

    pages: int = Field(nullable=False, default=1)

    color: bool = Field(nullable=False, default=False)

    status: JobStatus = Field(
        default=JobStatus.PENDING,
        nullable=False
    )

    cost: float = Field(nullable=False, default=0.0)

    created_at: datetime = Field(
        default_factory=generate_time,
        nullable=False
    )

    completed_at: datetime = Field(nullable=True, default=None)
