from pydantic import BaseModel
from datetime import datetime

from ..db.models.printer import PrinterStatus


class PrinterCreate(BaseModel):
    name: str
    location: str
    status: PrinterStatus


class PrinterCUPSUpdate(BaseModel):
    name: str
    location: str
    status: PrinterStatus


class PrinterRead(BaseModel):
    name: str
    location: str
    status: PrinterStatus
    price_per_page_bw: float
    admits_color: bool
    price_per_page_color: float
    updated_at: datetime


class PrinterAdminUpdate(BaseModel):
    price_per_page_bw: float | None = None
    admits_color: bool | None = None
    price_per_page_color: float | None = None
