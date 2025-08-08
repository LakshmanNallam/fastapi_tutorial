from pydantic import *

class GetUserLogin(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, val):
        if not 'gridlex' in val:
            raise ValueError('please provide your domain email')
        return val
    
class UserOutSchema(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode=True
