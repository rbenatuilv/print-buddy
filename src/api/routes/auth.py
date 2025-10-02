from fastapi import APIRouter, status
from fastapi import HTTPException

from ..dependencies.database import SessionDep
from ...schemas.user import UserCreate, UserRead, UserLogin
from ...schemas.token import AccessTokenResponse
from ...db.crud.user import UserService
from ...core.security import Security


user_service = UserService()
router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead
)
def register(
    user: UserCreate,
    session: SessionDep,
):
    
    email = user.email
    email_exists = user_service.email_exists(email, session)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    
    username = user.username
    username_exists = user_service.username_exists(username, session)
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    user.pwd = Security.hash_password(user.pwd)
    new_user = user_service.create_user(user, session)

    return new_user


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenResponse
)
def login(
    user: UserLogin,
    session: SessionDep
):
    
    valid = False

    username = user.username
    pwd = user.pwd

    user_db = user_service.get_user_by_username(username, session)
    if user_db is not None:
        valid = Security.verify_password(plain_pwd=pwd, hashed_pwd=user_db.pwd)

    if valid:
        payload = {"uid": str(user_db.id)}  # type: ignore
        token = Security.create_token(data=payload)

        return AccessTokenResponse(token=token)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Username or password incorrect"
    )
    