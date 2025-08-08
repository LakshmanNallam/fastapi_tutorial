# user routes
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
import schemas.schema_user as schema_user
from models import *
from database import *
from utils import *

router=APIRouter()

@router.post("/users/", response_model=schema_user.UserOut)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    user_dic=user.dict()
    
    print("user_dic",user_dic)
    # create hashed password
    hashed_password=create_hashed_password(user_dic["password"])
    user_dic["password"]=hashed_password

    print("user_dic",user_dic)
    db_user = User(**user_dic)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schema_user.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user