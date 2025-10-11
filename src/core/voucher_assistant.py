from fastapi import HTTPException, status
from sqlmodel import Session
import uuid

from ..db.crud.voucher import VoucherService
from ..db.crud.user import UserService
from ..db.models.voucher import VoucherStatus
from ..core.config import settings

from ..schemas.voucher import VoucherCreate, VoucherRedeem

from ..core.utils import generate_code, generate_time


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
    
    def voucher_redeemable(self, code, session):
        voucher = voucher_service.get_voucher_by_code(code, session)
        if voucher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voucher not found"
            )
        
        if voucher.status != VoucherStatus.ACTIVE:
            return False
        
        now = generate_time()
        delta = now - voucher.created_at

        if delta.total_seconds() > settings.EXP_TIME_VOUCHER_MIN * 60:
            voucher_service.expire_voucher(code, session)

            return False
        
        return True

    def redeem_voucher(
        self,
        user_id: str,
        code: str,
        session: Session
    ) -> bool:
        
        voucher = voucher_service.get_voucher_by_code(code, session)
        if voucher is None:
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
        
        amount = voucher.amount
        success = user_service.add_credit(user_id, amount, session)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to recharge user balance, try again"
            )
        
        voucher_data = VoucherRedeem(
            code=code,
            redeemed_by_id=uuid.UUID(user_id),
            redeemed_by_name=username
        )
        
        success = voucher_service.redeem_voucher(voucher_data, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voucher not found"
            )
        
        return success
        