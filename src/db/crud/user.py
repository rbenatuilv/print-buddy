from sqlmodel import Session, select

from ..models.user import User
from ...schemas.user import UserCreate


class UserService:


   ########################## CREATE #########################

    def create_user(
        self, 
        user_data: UserCreate,
        session: Session
    ) -> User:
        
        user = User(**user_data.model_dump())

        session.add(user)
        session.commit()

        return user
    
    ########################## READ ##########################

    def email_exists(
        self,
        email: str,
        session: Session 
    ) -> bool:

        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user is not None

    def username_exists(
        self,
        username: str,
        session: Session
    ):
        return self.get_user_by_username(username, session) is not None

    def get_user_by_username(
        self,
        username: str,
        session: Session
    ) -> User | None:

        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        return user
    
    def get_user_by_id(
        self,
        id: str,
        session: Session
    ):
        statement = select(User).where(User.id == id)
        user = session.exec(statement).first()

        return user
