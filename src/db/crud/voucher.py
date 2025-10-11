from sqlmodel import Session, select

from ..models.voucher import Voucher, VoucherStatus
from ...schemas.voucher import VoucherCreate, VoucherRedeem
from ...core.config import settings
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

        return old_code is None

    ########################## UPDATE #########################

    def redeem_voucher(
        self,
        voucher_data: VoucherRedeem,
        session: Session
    ) -> bool:
        
        code = voucher_data.code
        voucher = self.get_voucher_by_code(code, session)

        if voucher is None:
            return False
        
        if voucher.status != VoucherStatus.ACTIVE:
            return False
        
        now = generate_time()
        delta = now - voucher.created_at

        if delta.total_seconds() > settings.EXP_TIME_VOUCHER_MIN * 60:
            voucher.status = VoucherStatus.EXPIRED
            session.commit()
            
            return False 
        
        voucher.status = VoucherStatus.REDEEMED
        voucher.redeemed_by_id = voucher_data.redeemed_by_id
        voucher.redeemed_by_name = voucher_data.redeemed_by_name
        voucher.redeemed_at = generate_time()

        session.commit()
        return True
        
        

        