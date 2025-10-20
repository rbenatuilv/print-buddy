from fastapi import APIRouter, status, HTTPException
from ..dependencies.database import SessionDep
import json

from ...schemas.telegram import GenerateVoucher, TelegramID, UserBalance
from ...schemas.voucher import VoucherRead
from ...schemas.user import UserRead, UserAdminRead
from ...core.voucher_assistant import VoucherAssistant
from ...db.crud.user import UserService

from ...schemas.transaction import TransactionCreate
from ...db.crud.transaction import TransactionService
from ...db.models.transaction import TransactionType


router = APIRouter()
voucher_assistant = VoucherAssistant()
user_service = UserService()
tx_service = TransactionService()


TELEGRAM_ADMINS_FILE = "./src/core/telegram_admins.json"
with open(TELEGRAM_ADMINS_FILE) as f:
    TELEGRAM_TO_ADMIN = json.load(f)
    

@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=list[UserAdminRead]
)
def get_users(
    telegram_id: TelegramID,
    session: SessionDep
):
    """
    Return the list of all users for an authorized Telegram admin.
    """
    chat_id = telegram_id.chat_id
    admin_id = TELEGRAM_TO_ADMIN.get(str(chat_id))

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Telegram ID not allowed"
        )

    users = user_service.get_users(session)
    return users


@router.get(
    "/user/{username}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead
)
def get_user(
    username: str,
    telegram_id: TelegramID,
    session: SessionDep
):
    """
    Return the list of all users for an authorized Telegram admin.
    """
    chat_id = telegram_id.chat_id
    admin_id = TELEGRAM_TO_ADMIN.get(str(chat_id))

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Telegram ID not allowed"
        )

    user = user_service.get_user_by_username(username, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserRead
)
def get_me(
    telegram_id: TelegramID,
    session: SessionDep
):
    chat_id = telegram_id.chat_id
    admin_id = TELEGRAM_TO_ADMIN.get(str(chat_id))

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Telegram ID not allowed"
        )
    
    user = user_service.get_user_by_id(admin_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post(
    "/generate-voucher",
    status_code=status.HTTP_200_OK,
    response_model=VoucherRead
)
def generate_voucher(
    voucher_data: GenerateVoucher,
    session: SessionDep
):
    
    admin_chat_id = voucher_data.chat_id
    amount = voucher_data.amount

    admin_id = TELEGRAM_TO_ADMIN.get(str(admin_chat_id))
    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Telegram ID not allowed"
        )
    
    voucher = voucher_assistant.generate_voucher(
        admin_id, amount, session
    )

    return voucher


@router.patch(
    "/balance-adjust",
    status_code=status.HTTP_200_OK,
    response_model=UserRead
)
def adjust_balance(
    adjust_data: UserBalance,
    session: SessionDep 
):
    chat_id = adjust_data.chat_id
    admin_id = TELEGRAM_TO_ADMIN.get(str(chat_id))
    username = adjust_data.username

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Telegram ID not allowed"
        )
    
    user = user_service.get_user_by_username(username, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_id = str(user.id)
    amount = adjust_data.amount

    balance = user.balance
    diff = amount - balance
    if diff >= 0:
        user_service.add_credit(user_id, diff, session)
    else:
        user_service.discount_credit(user_id, -diff, session)

    balance = user_service.get_user_balance(user_id, session)
    admin = user_service.get_username_by_id(admin_id, session)

    tx_data = TransactionCreate(
        user_id=user.id,
        type=TransactionType.ADJUSTMENT,
        amount=diff,
        balance_after=balance,  # type: ignore
        note=f"Adjusted by {admin}"
    )

    tx_service.create_transaction(tx_data, session)

    return user


@router.patch(
    "/recharge",
    status_code=status.HTTP_200_OK,
)
def recharge_user(
    recharge_info: UserBalance,
    session: SessionDep
):
    
    chat_id = recharge_info.chat_id
    admin_id = TELEGRAM_TO_ADMIN.get(str(chat_id))
    username = recharge_info.username

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Telegram ID not allowed"
        )
    
    user = user_service.get_user_by_username(username, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_id = str(user.id)
    amount = recharge_info.amount

    success = user_service.add_credit(user_id, amount, session)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to recharge user"
        )
    
    balance = user_service.get_user_balance(user_id, session)
    admin = user_service.get_username_by_id(admin_id, session)

    tx_data = TransactionCreate(
        user_id=user.id,
        type=TransactionType.RECHARGE,
        amount=amount,
        balance_after=balance,  # type: ignore
        note=f"Recharge made by {admin}"
    )

    tx_service.create_transaction(tx_data, session)
    
    return { "success": True }
