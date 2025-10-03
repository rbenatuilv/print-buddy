from fastapi import APIRouter, status, HTTPException

from ..dependencies.token import TokenDep
from ..dependencies.database import SessionDep

from ...schemas.user import UserRead
from ...db.crud.user import UserService


router = APIRouter()
user_service = UserService()


@router.get(
    '/me',
    response_model=UserRead,
    status_code=status.HTTP_200_OK
)
def get_me(
    token: TokenDep,
    session: SessionDep
):
    user_id = token['uid']

    user = user_service.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
