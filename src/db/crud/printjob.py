from sqlmodel import Session, select

from ...db.models.printerjob import PrintJob
from ...schemas.printjob import PrintJobCreate


class PrintJobService:

    ########################## CREATE #########################

    def create_job(
        self,
        printjob_create: PrintJobCreate,
        session: Session,
    ):
        
        printjob = PrintJob(
            **printjob_create.model_dump()
        )

        session.add(printjob)
        session.commit()

        return printjob
