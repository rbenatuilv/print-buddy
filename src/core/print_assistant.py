from fastapi import status, HTTPException
from sqlmodel import Session
import uuid

from ..db.crud.user import UserService
from ..db.crud.printer import PrinterService
from ..db.crud.file import FileService
from ..db.crud.printjob import PrintJobService

from ..schemas.print import PrintOptions
from ..schemas.printjob import PrintJobCreate
from .cups import CUPSManager


user_service = UserService()
printer_service = PrinterService()
file_service = FileService()
pj_service = PrintJobService()

cups_mgr = CUPSManager()


class PrintAssistant:

    def get_file_to_print(
        self,
        user_id: str,
        file_id: str,
        session: Session
    ):
        check = False
        file = file_service.get_file_by_id(
            file_id, session
        )

        if file is not None:
            check = str(file.user_id) == user_id

        if not check:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found or not from user"
            )
        
        return file
    
    def get_printer(
        self,
        printer_name: str,
        session: Session
    ):
        printer = printer_service.get_printer_by_name(
            printer_name, session
        )

        if printer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Printer not found"
            )
        
        return printer
    
    def calculate_price(
        self,
        printer_name: str,
        color: bool,
        pages: int,
        session: Session
    ):
        
        printer = self.get_printer(printer_name, session)

        if color and not printer.admits_color:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Printer does not admit color printing"
            )
        
        if color:
            price = printer.price_per_page_color * pages
        else:
            price = printer.price_per_page_bw * pages

        return price
    
    def check_enough_credit(
        self, 
        user_id: str,
        cost: float,
        session: Session
    ):
        
        user = user_service.get_user_by_id(user_id, session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user.balance >= cost
    
        
    def send_print_job(
        self,
        user_id: str,
        file_id: str,
        printer_name: str,
        print_options: PrintOptions,
        session: Session
    ):
        
        file = self.get_file_to_print(user_id, file_id, session)
        
        pages = print_options.copies * file.pages  # type: ignore
        color = print_options.color

        cost = self.calculate_price(
            printer_name, color, pages, session
        )

        enough_credit = self.check_enough_credit(user_id, cost, session)

        if not enough_credit:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Not enough credit"
            )
        
        options = print_options.cups_options
        
        cups_job_id = cups_mgr.print_file(
            printer_name, 
            file.filepath,  # type: ignore
            options
        )

        if not cups_job_id:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to send job to printer"
            )
        
        user_service.discount_credit(user_id, cost, session)

        printer = self.get_printer(printer_name, session)

        pj = PrintJobCreate(
            cups_id=cups_job_id,
            user_id=uuid.UUID(user_id),
            printer_id=printer.id,
            file_id=file_id,  # type: ignore
            file_name=file.filename,  # type: ignore
            file_size=file.size_bytes,  # type: ignore
            pages=pages,
            copies=print_options.copies,
            color=print_options.color,
            cost=cost
        )


        pj_service.create_job(
            pj, session
        )

        return cups_job_id


        


        




        