from pydantic import BaseModel
from datetime import datetime
import uuid

from ..db.models.file import File
from ..db.models.printer import Printer

from .print import PrintOptions


class PrintJobCreate(BaseModel):
    user_id: str
    printer: Printer
    file: File
    print_options: PrintOptions
    pages: int
    cost: float

    @property
    def dump_on_DB(self) -> dict:
        return {
            "user_id": uuid.UUID(self.user_id),
            "printer_id": self.printer.id,
            "printer_name": self.printer.name,
            "file_id": self.file.id,
            "file_name": self.file.filename,
            "file_size": self.file.size_bytes,
            "pages": self.pages,
            "color": self.print_options.color,
            "cost": self.cost
        }


class PrintJobRead(BaseModel):
    printer_name: str
    file_name: str
    pages: int
    color: bool
    cost: float
    created_at: datetime
