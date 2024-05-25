from jose import JWTError, jwt
from firebase_admin import auth
from fastapi import HTTPException
from app.core.config import settings


def validate_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError("Invalid token")
        user = auth.get_user(user_id)
        return user
    except JWTError as e:
        raise HTTPException(status_code=401, detail=e) from e
