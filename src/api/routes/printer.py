from fastapi import APIRouter, status

from ..dependencies.database import SessionDep
from ..dependencies.token import TokenDep
from ...db.crud.printer import PrinterService
from ...schemas.printer import PrinterRead, PrinterCreate


printer_service = PrinterService()
router = APIRouter()


@router.get(
    "/all",
    response_model=list[PrinterRead],
    status_code=status.HTTP_200_OK
)
def get_printers(
    session: SessionDep
):
    printers = printer_service.get_all_printers(session)
    return printers


@router.post(
    "/",
    response_model=PrinterRead,
    status_code=status.HTTP_201_CREATED
)
def create_printer(
    printer_data: PrinterCreate,
    session: SessionDep
):
    new_printer = printer_service.create_printer(printer_data, session)
    return new_printer
    
