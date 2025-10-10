from fastapi import UploadFile
from pathlib import Path

from .utils import generate_time
from .config import settings


class FileManager:
    def __init__(self):
        self.max_sz = settings.MAX_FILE_SIZE_MB * 1024 * 1024

        self.extensions = {
            "application/pdf" : "pdf",
            "image/png": "png",
            "image/jpeg": "jpeg"
        }

    def is_valid_format(self, file: UploadFile) -> bool:
        file_type = file.content_type
        return file_type in self.extensions.keys()
    
    def generate_file_path(self, dirpath: Path, file: UploadFile):
        dirpath.mkdir(parents=True, exist_ok=True)
        
        if file.filename is None:
            ext = self.extensions[file.content_type]  # type: ignore
            file.filename = f"file_{generate_time().strftime('%Y%m%d_%H%M%S')}.{ext}"

        path = dirpath / file.filename

        counter = 1
        new_path = path
        while new_path.exists():
            file.filename = f"{path.stem}_({counter}){path.suffix}"
            new_path = path.with_stem(f"{path.stem}_({counter})")
            counter += 1

        return new_path

    def save_file(self, path: Path, file: UploadFile) -> int:
        """
        Receives a ``path`` object and a ``file`` object and saves it
        to the corresponding directory. Returns the size of file 
        in bytes. -1 is returned if file exceeds max size.
        """

        total_bytes = 0
        with open(path, "wb") as buffer:
            while chunk := file.file.read(1024 * 1024):
                total_bytes += len(chunk)
                if total_bytes > self.max_sz:
                    buffer.close()
                    path.unlink(missing_ok=True)

                    return -1
                buffer.write(chunk)

        return total_bytes
    
    def delete_file(self, path: Path) -> bool:
        if not path.exists():
            return False
        
        try:
            path.unlink(missing_ok=True)
            return True
        except Exception as e:
            return False
