from sqlmodel import Session, select
import uuid

from ..models.file import File
from ...schemas.file import FileCreate


class FileService:

    ################## CREATE ####################

    def create_file(
        self, 
        user_id: str,
        file_data: FileCreate,
        session: Session
    ):
        
        file = File(
            user_id=uuid.UUID(user_id),
            **file_data.model_dump()
        )

        session.add(file)
        session.commit()

        return file

    ################## READ ####################

    def get_files_by_user_id(
        self,
        id: str,
        session: Session
    ):
        stmt = select(File).where(File.user_id == id)
        files = session.exec(stmt).all()

        return files
    
    def is_file_from_user(
        self,
        file_id: str,
        user_id: str,
        session: Session
    ):
        stmt = select(File).where(File.id == file_id)
        file = session.exec(stmt).first()

        if file is None:
            return False
        
        return str(file.user_id) == user_id
    
    ################## DELETE ####################

    def delete_file(
        self,
        file_id: str,
        session: Session
    ):
        stmt = select(File).where(File.id == file_id)
        file = session.exec(stmt).first()

        if file is None:
            return None
        
        session.delete(file)
        session.commit()
        return file
