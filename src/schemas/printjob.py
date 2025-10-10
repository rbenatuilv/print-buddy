from pydantic import BaseModel
import uuid


class PrintJobCreate(BaseModel):

    cups_id: str
    user_id: uuid.UUID
    printer_id: uuid.UUID
    file_id: uuid.UUID
    file_name: str
    file_size: int
    pages: int
    copies: int
    color: bool
    cost: float

