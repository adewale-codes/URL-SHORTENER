from pydantic import BaseModel

class CreateURLRequest(BaseModel):
    original_url: str
    custom_alias: str = None

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str 