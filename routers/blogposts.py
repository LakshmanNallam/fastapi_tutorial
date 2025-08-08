# user routes
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
import schemas.schema_blogpost as schema_blogpost
import schemas.schema_auth as schema_auth
import utils
from models import *
from database import *


router=APIRouter()

@router.post("/",response_model=schema_blogpost.outBlogPost)
def create_post(post_payload: schema_blogpost.createBlogPost, db: Session = Depends(get_db),user_details:int=Depends(utils.get_user_details)):
    
    post_payload=post_payload.dict()
    user_obj = db.query(User).filter(User.id == post_payload["user_id"]).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    print("user_details",user_details)
    new_post_ins = BlogPosts(content=post_payload["content"], user_id=user_obj.id)
    db.add(new_post_ins)
    db.commit()
    db.refresh(new_post_ins)
    print(post_payload)
    print("new_post_ins",new_post_ins)
    return {"result":new_post_ins}

