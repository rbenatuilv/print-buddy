from pydantic import BaseModel
from datetime import datetime

from ..db.models.printer import PrinterStatus


class PrinterCreate(BaseModel):
    name: str
    location: str
    status: PrinterStatus


class PrinterStatusUpdate(BaseModel):
    name: str
    location: str
    status: PrinterStatus


class PrinterRead(BaseModel):
    name: str
    location: str
    status: PrinterStatus
    price_per_page: float
    updated_at: datetime
