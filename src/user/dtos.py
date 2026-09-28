from pydantic import BaseModel

class UserSchema(BaseModel):
    name : str
    username : str | None =None
    password : str | None = None
    email : str

class ResponseSchema(BaseModel):
    id :int 
    username: str

class LoginSchema(BaseModel):
    username: str |None = None,
    password: str |None = None