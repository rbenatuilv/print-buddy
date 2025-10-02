from bcrypt import hashpw, gensalt, checkpw
from datetime import timedelta
from jose import jwt, JWTError
import uuid

from .utils import generate_time
from .config import settings


class Security:
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        A class method to hash a password. Returns the hashed password
        """
        return hashpw(password.encode(), gensalt()).decode()
    
    @classmethod
    def verify_password(cls, plain_pwd: str, hashed_pwd: str) -> bool:
        """
        Verifies if the plain password coincides with the hashed password.
        Returns True or False
        """
        return checkpw(plain_pwd.encode(), hashed_pwd.encode())
    
    @classmethod
    def create_token(cls, data: dict) -> str:
        """
        Creates a JWT token.
        """
        delta = timedelta(minutes=settings.ACCESS_TOKEN_EXP_MIN)
        exp_time = generate_time() + delta

        to_encode = data.copy()

        payload = {
            "exp": exp_time,
            "jti": str(uuid.uuid4())
        }

        to_encode.update(payload)

        token = jwt.encode(
            claims=to_encode,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

        return token
    
    @classmethod
    def decode_token(cls, token: str) -> dict | None:
        """
        Decodes a JWT token
        """
        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            return payload
        
        except JWTError as e:
            print("INVALID OR EXPIRED TOKEN")
            return None
