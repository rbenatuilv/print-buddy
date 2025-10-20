from fastapi import APIRouter, status, HTTPException
import json

from ..dependencies.token import TokenDep, AdminTokenDep
from ..dependencies.database import SessionDep

from ...db.crud.transaction import TransactionService
from ...db.models.transaction import TransactionType
from ...schemas.transaction import TransactionRead, TransactionCreate

from ...db.crud.user import UserService


router = APIRouter()
tx_service = TransactionService()
user_service = UserService()


@router.get(
    "/me",
    response_model=list[TransactionRead],
    status_code=status.HTTP_200_OK
)
def get_my_transactions(
    token: TokenDep,
    session: SessionDep
):
    user_id = token.credentials

    tx_s = tx_service.get_transactions_from_user(user_id, session)

    return tx_s


@router.get(
    "/recharge-info",
    status_code=status.HTTP_200_OK
)
def get_recharge_info(
    token: TokenDep
):
    with open("./src/core/recharge_info.json") as f:
        return json.load(f)