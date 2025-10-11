from sqlmodel import Session, select

from ..models.voucher import Voucher, VoucherStatus
from ...schemas.voucher import VoucherCreate, VoucherRedeem
from ...core.utils import generate_time


class VoucherService:

    ########################## CREATE #########################

    def create_voucher(
        self,
        voucher_data: VoucherCreate,
        session: Session
    ):
        voucher = Voucher(**voucher_data.model_dump())

        session.add(voucher)
        session.commit()

        return voucher
    
    ########################## READ #########################

    def get_voucher_by_code(
        self,
        code: str,
        session: Session
    ):
        stmt = select(Voucher).where(Voucher.code == code)
        voucher = session.exec(stmt).first()

        return voucher
    
    def code_exists(
        self,
        code: str,
        session: Session
    ):
        stmt = select(Voucher.code).where(Voucher.code == code)
        old_code = session.exec(stmt).first()

        return old_code is not None
    
    def get_amount_by_code(
        self,
        code: str,
        session: Session
    ):
        stmt = select(Voucher.amount).where(Voucher.code == code)
        amount = session.exec(stmt).first()
        return amount

    ########################## UPDATE #########################

    def expire_voucher(self, code: str, session: Session):
        voucher = self.get_voucher_by_code(code, session)
        if voucher is None:
            return False
        
        voucher.status = VoucherStatus.EXPIRED
        session.commit()
        return True

    def redeem_voucher(
        self,
        voucher_data: VoucherRedeem,
        session: Session
    ) -> bool:
        
        code = voucher_data.code
        voucher = self.get_voucher_by_code(code, session)
        if voucher is None:
            return False

        voucher.status = VoucherStatus.REDEEMED
        voucher.redeemed_by_id = voucher_data.redeemed_by_id
        voucher.redeemed_by_name = voucher_data.redeemed_by_name
        voucher.redeemed_at = generate_time()

        session.commit()
        return True
        
        

        