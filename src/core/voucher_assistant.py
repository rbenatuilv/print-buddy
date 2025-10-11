from fastapi import HTTPException, status
from sqlmodel import Session
import uuid

from ..db.crud.voucher import VoucherService
from ..db.crud.user import UserService

from ..schemas.voucher import VoucherCreate, VoucherRedeem

from ..core.utils import generate_code


voucher_service = VoucherService()
user_service = UserService()


class VoucherAssistant:

    def __init__(self):
        self.MAX_CODE_GEN_RETRIES = 10

    def generate_unique_code(self, session: Session) -> str:
        code = generate_code()

        retry = 0
        exists = voucher_service.code_exists(code, session)
        while retry < self.MAX_CODE_GEN_RETRIES and exists:
            code = generate_code()
            exists = voucher_service.code_exists(code, session)
            retry += 1

        if retry >= self.MAX_CODE_GEN_RETRIES:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to generate code, too many collisions"
            )
        
        return code

    def generate_voucher(
        self, 
        admin_id: str, 
        amount: float, 
        session: Session
    ):

        username = user_service.get_username_by_id(admin_id, session)

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        code = self.generate_unique_code(session)

        voucher_data = VoucherCreate(
            code=code,
            amount=amount,
            created_by_id=uuid.UUID(admin_id),
            created_by_name=username
        )

        voucher = voucher_service.create_voucher(
            voucher_data, session
        )

        return voucher

    def redeem_voucher(
        self,
        user_id: str,
        code: str,
        session: Session
    ) -> bool:
        
        exists = voucher_service.code_exists(code, session)
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voucher not found"
            )
        
        username = user_service.get_username_by_id(user_id, session)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        voucher_redeem = VoucherRedeem(
            code=code,
            redeemed_by_id=uuid.UUID(user_id),
            redeemed_by_name=username
        )

        success = voucher_service.redeem_voucher(
            voucher_redeem, session
        )

        return success
