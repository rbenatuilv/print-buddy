from sqlmodel import Session, select
import uuid

from ...db.models.printerjob import PrintJob
from ...schemas.printjob import PrintJobCreate


class PrintJobService:

    ########################## CREATE #########################

    def create_job(
        self,
        cups_id: str,
        printjob: PrintJobCreate,
        session: Session,
    ) -> PrintJob:
        
        new_printjob = PrintJob(
            cups_id=cups_id,
            user_id=uuid.UUID(printjob.user_id),
            printer_id=printjob.printer.id,
            printer_name=printjob.printer.name,
            file_id=printjob.file.id,
            file_name=printjob.file.filename,
            file_size=printjob.file.size_bytes,
            pages=printjob.file.pages,
            copies=printjob.print_options.copies,
            color=printjob.print_options.color
        )

        session.add(new_printjob)
        session.commit()

        return new_printjob
