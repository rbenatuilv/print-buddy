from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session, select
import json
import asyncio
from datetime import timedelta
from pathlib import Path

from .cups_manager import CUPSManager
from ..db.main import engine

from ..db.crud.printer import PrinterService
from ..db.crud.printjob import PrintJobService
from ..db.crud.user import UserService
from ..db.crud.transaction import TransactionService
from ..db.crud.file import FileService

from ..db.models.printerjob import ERROR_STATUS
from ..db.models.transaction import TransactionType
from ..schemas.printer import PrinterCUPSUpdate
from ..schemas.transaction import TransactionCreate

from ..core.utils import generate_time
from ..core.file_manager import FileManager


printer_service = PrinterService()
pj_service = PrintJobService()
user_service = UserService()
tx_service = TransactionService()
file_service = FileService()
fm = FileManager()

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

    def update_printers_sync(self):
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

    def update_jobs_sync(self):

        with Session(engine) as session:
            jobs_to_update = pj_service.get_transitory_status_jobs(session)
        
            if not jobs_to_update:
                return
            
            for job_id, cups_id, status in jobs_to_update:
                new_status = cups_mgr.get_job_status(int(cups_id))
                
                if new_status is None:
                    continue

                if status != new_status:
                    job = pj_service.update_job_status(str(job_id), new_status, session)
                    if job is not None and new_status in ERROR_STATUS:
                        user_service.add_credit(str(job.user_id), job.cost, session)

                        balance = user_service.get_user_balance(str(job.user_id), session)

                        tx_data = TransactionCreate(
                            user_id=job.user_id,
                            type=TransactionType.REFUND,
                            amount=job.cost,
                            balance_after=balance,  # type: ignore
                            note=f"Refunded from file print: {job.file_name}"
                        )

                        tx_service.create_transaction(tx_data, session)

    def delete_old_files_sync(self):
        timeframe = generate_time() - timedelta(days=1)

        with Session(engine) as session:
            old_files = file_service.get_old_files(
                timeframe, session
            )

            for file in old_files:
                file_id = file.id
                file_service.delete_file(str(file_id), session)
                path = Path(file.filepath)
                fm.delete_file(path)

    async def update_printers(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.update_printers_sync)

    async def update_jobs(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.update_jobs_sync)

    async def delete_old_files(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.delete_old_files_sync)

    def start(self, *args, **kwargs):
        self.add_job(self.update_printers, "interval", seconds=60)
        self.add_job(self.update_jobs, "interval", seconds=5)
        self.add_job(self.delete_old_files, "interval", seconds=7200)
        
        super().start(*args, **kwargs)
