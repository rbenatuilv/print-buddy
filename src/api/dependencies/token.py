from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request, Depends
from typing import Annotated

from ...core.security import Security



class AuthCreds(HTTPAuthorizationCredentials):

    def __init__(self, token: dict, scheme: str = ''):
        self.token = token
        super().__init__(scheme=scheme, credentials='')

    def __getitem__(self, index):
        return self.token[index]


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = Security.decode_token(creds.credentials) if creds else None

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access"
            )
        
        if creds is not None:
            return AuthCreds(token=token, scheme=creds.scheme)
    

TokenDep = Annotated[
    AuthCreds, Depends(TokenBearer())
]
