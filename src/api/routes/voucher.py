from fastapi import APIRouter, status, HTTPException

from ..dependencies.token import TokenDep, AdminTokenDep
from ..dependencies.database import SessionDep

from ...schemas.voucher import VoucherRead, RedeemSuccess

from ...core.voucher_assistant import VoucherAssistant


router = APIRouter()
voucher_assistant = VoucherAssistant()


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
    success = voucher_assistant.redeem_voucher(
        user_id, code, session
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher does not exist or is no lonnger valid"
        )
    
    return {"success": success}
