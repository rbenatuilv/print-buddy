from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from enum import Enum

from ...core.utils import generate_time


class PrinterStatus(str, Enum):
    IDLE = "idle"
    PRINTING = "printing"
    STOP = "stopped"

class Printer(SQLModel, table=True):

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, 
        primary_key=True
    )

    name: str = Field(nullable=False, index=True)

    location: str = Field(nullable=True)

    status: PrinterStatus = Field(
        nullable=False, 
        default=PrinterStatus.IDLE
    )

    price_per_page_bw: float = Field(nullable=False, default=0.0)

    admits_color: bool = Field(default=False, nullable=False)

    price_per_page_color: float = Field(default=0.0)

    created_at: datetime = Field(
        default_factory=generate_time, 
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=generate_time, 
        nullable=False
    )
