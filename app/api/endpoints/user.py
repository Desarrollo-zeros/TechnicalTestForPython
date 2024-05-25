from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import oauth2_scheme,  get_user_service_request
from app.domain.contracts.services.I_user_service import IUserService
from app.domain.inputs.user_login_input import UserLogin
from app.domain.inputs.user_register_input import UserRegistration

router = APIRouter()


@router.post("/users/register")
async def register(user_details: UserRegistration, user_service: IUserService = Depends(get_user_service_request)):
    user = user_service.register_user(user_details)
    return {"message": "Usuario registrado con existo", "uid": user.uid}


@router.post("/users/login")
async def login(user_credentials: UserLogin, user_service: IUserService = Depends(get_user_service_request)):
    token = user_service.login_user(user_credentials)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme), user_service: IUserService = Depends(get_user_service_request)):
    user = user_service.get_user_from_token(token)
    return user


@router.post("/users/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: IUserService = Depends(get_user_service_request)):
    user_credentials = UserLogin(email=form_data.username, password=form_data.password)
    token = user_service.login_user(user_credentials)
    return {"access_token": token, "token_type": "bearer"}
