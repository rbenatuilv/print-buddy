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
            **printjob.dump_on_DB
        )

        session.add(new_printjob)
        session.commit()

        return new_printjob
