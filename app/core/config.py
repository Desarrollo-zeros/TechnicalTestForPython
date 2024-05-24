import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.SECRET_KEY: str = os.getenv("SECRET_KEY")
        self.ALGORITHM: str = "HS256"
        self.DATABASE_URL: str = os.getenv("DATABASE_URL")
        self.DATA_DIRECTORY: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', os.getenv("DATA_DIRECTORY")))
        self.MAX_SIZE_CACHE: int = int(os.getenv("MAX_SIZE_CACHE"))
        self.TTL_CACHE: int = int(os.getenv("TTL_CACHE"))
        self.URL_DATA_EXAMPLE = (os.getenv("URL_DATA_EXAMPLE"))
        self.ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.ml_models = {}
        self.SERVICE_ACCOUNT_KEY = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', os.getenv("SERVICE_ACCOUNT_KEY")))
        self.__initialized = True


settings = Settings()
