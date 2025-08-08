import json
from pydantic import *

class createBlogPost(BaseModel):
    content: str
    user_id: int

class PassBlogPost(createBlogPost):
    json_data:str

    @validator("json_data")
    def valid_json_data(cls,v):
        parsed_jsn=json.loads(v)
        print("parsed_jsn",parsed_jsn)
        createBlogPost(**parsed_jsn)
        return v

class getBlogPost(createBlogPost):
    pass
    
    class Config:
        orm_mode=True
        

class outBlogPost(BaseModel):
    result : getBlogPost

        