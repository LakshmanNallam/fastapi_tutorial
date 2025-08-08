from pydantic import *

class createBlogPost(BaseModel):
    content: str
    user_id: int

class getBlogPost(createBlogPost):
    pass
    
    class Config:
        orm_mode=True
        

class outBlogPost(BaseModel):
    result : getBlogPost

        