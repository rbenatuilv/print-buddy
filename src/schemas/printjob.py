from pydantic import BaseModel
from datetime import datetime

from ..db.models.file import File
from ..db.models.printer import Printer

from .print import PrintOptions


class PrintJobCreate(BaseModel):
    user_id: str
    printer: Printer
    file: File
    print_options: PrintOptions
    cost: float


class PrintJobRead(BaseModel):
    printer_name: str
    file_name: str
    pages: int
    copies: int
    color: bool
    cost: float
    created_at: datetime
