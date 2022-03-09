from pydantic import BaseModel


class JWTUser(BaseModel):
    user_id: int = None
    username: str
    password: str
    disabled: bool = False
    role: str = None
