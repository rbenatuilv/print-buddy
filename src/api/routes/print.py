from fastapi import APIRouter, status, HTTPException

from ..dependencies.token import TokenDep
from ..dependencies.database import SessionDep

from ...schemas.print import PrintJobResponse, PrintOptions
from ...db.crud.user import UserService
from ...db.crud.printer import PrinterService
from ...db.crud.file import FileService
from ...core.cups import CUPSManager
from ...core.print_assistant import PrintAssistant


router = APIRouter()

print_assistant = PrintAssistant()


@router.post(
    '/{printer_name}/{file_id}',
    response_model=PrintJobResponse,
    status_code=status.HTTP_200_OK
)
def print_file(
    printer_name: str,
    file_id: str,
    print_options: PrintOptions,
    token: TokenDep,
    session: SessionDep
):
    user_id = token.credentials

    cups_job_id = print_assistant.send_print_job(
        user_id, file_id, printer_name, print_options, session
    )

    


    





