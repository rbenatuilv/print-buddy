from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session, select
import json

from .cups import CUPSManager
from ..db.main import engine
from ..db.crud.printer import PrinterService
from ..schemas.printer import PrinterCUPSUpdate


printer_service = PrinterService()
cups_mgr = CUPSManager()


class Scheduler(AsyncIOScheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.printers_data = []

    def _normalize_data(self, printers_data: list[dict]) -> str:
        return json.dumps(printers_data, sort_keys=True)

    def check_printer_changes(self, printers_data: list[dict]) -> bool:
        if not self.printers_data:
            self.printers_data = printers_data
            return True

        old_state = self._normalize_data(self.printers_data)
        new_state = self._normalize_data(printers_data)

        if old_state != new_state:
            self.printers_data = printers_data
            return True

        return False

    def update_printers(self):
        printers_data = cups_mgr.get_printers()

        if not self.check_printer_changes(printers_data):
            return

        with Session(engine) as session:
            for data in printers_data:

                print_update = PrinterCUPSUpdate(**data)
                printer_service.update_printer_CUPS(
                    printer_update=print_update,
                    session=session
                )

    def start(self, *args, **kwargs):
        self.add_job(self.update_printers, "interval", seconds=60)
        super().start(*args, **kwargs)
