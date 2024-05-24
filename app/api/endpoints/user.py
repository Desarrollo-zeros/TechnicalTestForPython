from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import oauth2_scheme
from app.domain.inputs.user_login_input import UserLogin
from app.domain.inputs.user_register_input import UserRegistration
from app.services.auth_service import AuthService

router = APIRouter()
@router.post("/users/register")
async def register(user_details: UserRegistration):
    try:
        user = AuthService().register_user(user_details)
        return {"message": "Usuario registrado con existo", "uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registro ha fallado: {str(e)}")

@router.post("/users/login")
async def login(user_credentials: UserLogin):
    try:
        token = AuthService().login_user(user_credentials)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Logeo ha fallado: {str(e)}")

@router.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = AuthService().get_user_from_token(token)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token Invalido: {str(e)}")


@router.post("/users/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_credentials = UserLogin(email=form_data.username, password=form_data.password)
    token = AuthService().login_user(user_credentials)
    return {"access_token": token, "token_type": "bearer"}