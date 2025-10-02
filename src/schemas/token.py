from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    token: str
