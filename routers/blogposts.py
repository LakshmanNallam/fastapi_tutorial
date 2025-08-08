# user routes
from fastapi import FastAPI, Depends, HTTPException,APIRouter,File,UploadFile,Form

#jkadsfd
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
import schemas.schema_blogpost as schema_blogpost
import schemas.schema_auth as schema_auth
import utils
from models import *
from database import *
import os

router=APIRouter()

os.makedirs('uploads',exist_ok=True)

# user_details:int=Depends(utils.get_user_details)
# response_model=schema_blogpost.outBlogPost
@router.post("/")
async def create_post(post_payload: str=Form(...),file:Optional[UploadFile]=File(None), db: Session = Depends(get_db)):
    

    validated_payload_dict=schema_blogpost.createBlogPost.parse_raw(post_payload).dict()
    user_obj = db.query(User).filter(User.id == validated_payload_dict["user_id"]).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")

    file_path=None
    if file:
        file_path=os.path.join("uploads",file.filename)
        print("file_path",file_path)
        with open(file_path,"wb") as f:
            f.write(await file.read())

    new_post_ins = BlogPosts(content=validated_payload_dict["content"], user_id=user_obj.id,file_path=file_path)
    db.add(new_post_ins)
    db.commit()
    db.refresh(new_post_ins)

    return {"result":"HI"}

@router.get("/post/{id}")
def getPost(id:int,db: Session = Depends(get_db)):
    post_detail=db.query(BlogPosts).filter(BlogPosts.id == id).first()
    
    return FileResponse(path=post_detail.file_path, filename="filename", media_type="application/octet-stream")