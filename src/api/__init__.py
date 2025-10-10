from fastapi import APIRouter, status

from .routes import auth, user, printer, file


router = APIRouter()

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
def root():
    return {
        "message": "Hello World"
    }


router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(printer.router, prefix="/printers", tags=["printers"])
router.include_router(file.router, prefix="/files", tags=["files"])
