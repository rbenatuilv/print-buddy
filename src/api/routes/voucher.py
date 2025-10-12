from fastapi import APIRouter, status, HTTPException

from ..dependencies.token import TokenDep, AdminTokenDep
from ..dependencies.database import SessionDep

from ...schemas.voucher import VoucherRead, RedeemSuccess
from ...db.crud.voucher import VoucherService
from ...core.voucher_assistant import VoucherAssistant


router = APIRouter()
voucher_assistant = VoucherAssistant()
voucher_service = VoucherService()


@router.post(
    '/generate/{amount}',
    response_model=VoucherRead,
    status_code=status.HTTP_201_CREATED
)
def generate_voucher(
    amount: float,
    token: AdminTokenDep,
    session: SessionDep
):
    admin_id = token.credentials
    voucher = voucher_assistant.generate_voucher(
        admin_id, amount, session
    )

    return voucher


@router.post(
    '/redeem/{code}',
    response_model=RedeemSuccess,
    status_code=status.HTTP_201_CREATED
)
def redeem_voucher(
    code: str,
    token: TokenDep,
    session: SessionDep
):
    
    user_id = token.credentials
    
    redeemable = voucher_assistant.voucher_redeemable(code, session)
    if not redeemable:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Voucher not redeemable"
        )
    
    success = voucher_assistant.redeem_voucher(
        user_id, code, session
    )
    
    return {"success": success}


@router.post(
    "/revoke/{code}",
    response_model=VoucherRead,
    status_code=status.HTTP_200_OK
)
def revoke_voucher(
    code: str,
    token: AdminTokenDep,
    session: SessionDep
):
    voucher = voucher_service.revoke_voucher(code, session)
    if voucher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher not found"
        )
    
    return voucher
