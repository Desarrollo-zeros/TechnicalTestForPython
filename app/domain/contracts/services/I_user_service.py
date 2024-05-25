from abc import ABC, abstractmethod
from typing import Dict

from app.domain.inputs.user_login_input import UserLogin
from app.domain.inputs.user_register_input import UserRegistration


class IUserService(ABC):

    @abstractmethod
    def register_user(self, user_details: UserRegistration) -> Dict[str, str]:
        pass

    @abstractmethod
    def login_user(self, user_credentials: UserLogin) -> str:
        pass

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def get_user_from_token(self, token: str) -> Dict[str, str]:
        pass
