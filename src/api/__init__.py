from fastapi import APIRouter, status

from .routes import auth, user, printer, file, print, voucher, transaction, telegram


router = APIRouter()

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
def root():
    return {
        "message": "Hello World"
    }

@router.get("/health")
def health():
    return {"status": "ok"}


router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(printer.router, prefix="/printers", tags=["printers"])
router.include_router(file.router, prefix="/files", tags=["files"])
router.include_router(print.router, prefix="/print", tags=["print"])
router.include_router(voucher.router, prefix="/vouchers", tags=["vouchers"])
router.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
router.include_router(telegram.router, prefix="/telegram", tags=["telegram"])
