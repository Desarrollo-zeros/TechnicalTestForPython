from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from firebase_admin import auth
from jwt import ExpiredSignatureError

from app.domain.inputs.user_login_input import UserLogin
from app.domain.inputs.user_register_input import UserRegistration
from fastapi import HTTPException
from app.core.config import settings


class AuthService:
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def register_user(self, user_details: UserRegistration):
        user = auth.create_user(
            email=user_details.email,
            password=user_details.password,
            display_name=user_details.display_name
        )
        return user

    def login_user(self, user_credentials: UserLogin):
        user = auth.get_user_by_email(user_credentials.email)
        token = self.create_access_token({"sub": user.uid})
        return token

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc)  + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_user_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            user = auth.get_user(user_id)
            return {"uid": user.uid, "email": user.email, "display_name": user.display_name}
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")