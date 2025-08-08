# user routes
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi import HTTPException as FastApiHTTPException
from sqlalchemy.orm import Session
import schemas.schema_auth as schema_auth
from models import *
from database import *
from utils import *

router=APIRouter()

@router.post("/login")
def login_user(user_payload: schema_auth.GetUserLogin, db: Session = Depends(get_db)):
    
    user_payload=user_payload.dict()

    user_obj = db.query(User).filter(User.email == user_payload["email"]).first()
    if not user_obj:
        print("HTTPException",HTTPException)
        raise FastApiHTTPException(status_code=404, detail="Please create account / Invalid cred")
    
    # check password is correct or not
    if not verify_hashed_password(user_payload["password"],user_obj.password):
        print("HTTPException",FastApiHTTPException)
        raise FastApiHTTPException(status_code=404, detail="Please create account / Invalid cred")

    # generate the jwt token
    token=create_jwt_token(user_payload["email"])
    
    return {"user_id":user_obj.id,"user_email":user_obj.email,"jwt":token}


@router.get("/verifyjwt",response_model=schema_auth.UserOutSchema)
def verify_jwt(user_details:int=Depends(get_user_details)):
    print("user_details",user_details)
    
    return user_details
