from pydantic import BaseModel


class User(BaseModel):
    uid: str
    email: str
    display_name: str
    created_at: str
