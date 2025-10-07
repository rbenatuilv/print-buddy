from fastapi import APIRouter, status, HTTPException

from ..dependencies.token import TokenDep
from ..dependencies.database import SessionDep

from ...schemas.user import UserRead, UserUpdate
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
    user_id = token.credentials

    user = user_service.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.patch(
    '/me',
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def update_me(
    user_data: UserUpdate,
    token: TokenDep,
    session: SessionDep
):
    
    user_id = token.credentials
    is_admin = user_service.user_is_admin(user_id, session)

    if not is_admin:
        user_data.name = None
        user_data.surname = None
        user_data.username = None

    if user_data.email is not None:
        email_exists = user_service.email_exists(user_data.email, session)

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email already exists'
            )
        
    if user_data.username is not None:
        username_exists = user_service.username_exists(user_data.username, session)

        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Username already exists'
            )

    user = user_service.update_user(user_id, user_data, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return user


@router.get(
    '',
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK
)
def get_users(
    token: TokenDep,
    session: SessionDep
):
    user_id = token.credentials

    is_admin = user_service.user_is_admin(user_id, session)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User not authorized'
        )
    
    users = user_service.get_users(session)

    return users
