from pydantic import BaseModel


class TelegramID(BaseModel):
    chat_id: str


class GenerateVoucher(TelegramID):
    amount: float


class UserBalance(TelegramID):
    username: str
    amount: float