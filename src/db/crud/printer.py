from sqlmodel import Session, select

from ..models.printer import Printer
from ...schemas.printer import PrinterCreate, PrinterStatusUpdate
from ...core.utils import generate_time


class PrinterService:

    def create_printer(
        self, 
        printer_data: PrinterCreate,
        session: Session
    ):
        
        printer = Printer(**printer_data.model_dump())
        session.add(printer)
        session.commit()

        return printer
    
    def update_printer_status(
        self,
        printer_update: PrinterStatusUpdate,
        session: Session
    ):
        name = printer_update.name
        stmt = select(Printer).where(Printer.name == name)
        printer = session.exec(stmt).first()

        if printer is None:
            new_printer = PrinterCreate(**printer_update.model_dump())
            return self.create_printer(new_printer, session)

        printer.location = printer_update.location
        printer.status = printer_update.status
        printer.updated_at = generate_time()

        session.commit()
        return printer
    
    def get_all_printers(self, session: Session):
        stmt = select(Printer)
        printers = session.exec(stmt).all()

        return printers



