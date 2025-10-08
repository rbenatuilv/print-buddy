from fastapi import APIRouter, status, HTTPException

from ..dependencies.database import SessionDep
from ..dependencies.token import TokenDep
from ...db.crud.printer import PrinterService
from ...db.crud.user import UserService
from ...schemas.printer import PrinterRead, PrinterCreate


printer_service = PrinterService()
user_service = UserService()

router = APIRouter()


@router.get(
    "",
    response_model=list[PrinterRead],
    status_code=status.HTTP_200_OK
)
def get_printers(
    session: SessionDep
):
    printers = printer_service.get_all_printers(session)
    return printers


@router.post(
    "",
    response_model=PrinterRead,
    status_code=status.HTTP_201_CREATED
)
def create_printer(
    printer_data: PrinterCreate,
    token: TokenDep,
    session: SessionDep
):
    user_id = token.credentials
    is_admin = user_service.user_is_admin(user_id, session)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User not authorized'
        )

    new_printer = printer_service.create_printer(printer_data, session)
    return new_printer


# @router.patch(

# )
    
