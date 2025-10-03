from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session, select

from .cups import CUPSManager
from ..db.main import engine
from ..db.crud.printer import PrinterService
from ..schemas.printer import PrinterStatusUpdate


printer_service = PrinterService()
cups_mgr = CUPSManager()


class Scheduler(AsyncIOScheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def update_printers(self):
        printers_data = cups_mgr.get_printers()

        with Session(engine) as session:
            for data in printers_data:

                print_update = PrinterStatusUpdate(**data)
                printer_service.update_printer_status(
                    printer_update=print_update,
                    session=session
                )

    def start(self, *args, **kwargs):
        self.add_job(self.update_printers, "interval", seconds=10)
        super().start(*args, **kwargs)
