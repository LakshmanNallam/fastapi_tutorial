from pydantic import *

class UserBase(BaseModel):
    name: str
    email: str
    password:str

class UserCreate(UserBase):
    @validator("email")
    def validate_email(cls, val):
        if not 'gridlex' in val:
            raise ValueError('please provide your domain email')
        return val


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
