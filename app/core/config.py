import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATA_DIRECTORY: str = os.getenv("DATA_DIRECTORY")


settings = Settings()
