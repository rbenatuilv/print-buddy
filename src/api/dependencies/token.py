from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request, Depends
from typing import Annotated

from ...core.security import Security


class TokenBearer:

    def __init__(self):
        self.scheme = HTTPBearer()

    async def __call__(self, request: Request) -> dict:
        creds: HTTPAuthorizationCredentials | None = await self.scheme(request)

        token = Security.decode_token(creds.credentials) if creds else None

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access"
            )
        
        return token
    

TokenDep = Annotated[
    dict, Depends(TokenBearer())
]
