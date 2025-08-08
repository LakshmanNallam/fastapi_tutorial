from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone
from models import User
from database import get_db
from fastapi.security import OAuth2PasswordBearer

# Create password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_hashed_password(user_plain_password):

    hashed_password = pwd_context.hash(user_plain_password)
    return hashed_password

def verify_hashed_password(user_plain_password,stored_hash):
    is_correct_password=pwd_context.verify(user_plain_password,stored_hash)
    return is_correct_password


# Define your secret key (keep this secure and never expose it)
SECRET_KEY = "hQ5AfeJgh3b1HiV4Bi7xoty1u2EEjRf+JrV9DYuwOzc="
# Define the algorithm to be used for signing (e.g., HS256)
ALGORITHM = "HS256"

def create_jwt_token(user_email: str, minutes_to_expire: int = 30):

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=minutes_to_expire)
    print("expire_time",expire_time)
    payload = {
        "user_email": user_email,
        "exp": expire_time
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_jwt_token(token):
    # Decoding for verification (optional, for demonstration)
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {decoded_payload}")

        return decoded_payload
    
    except jwt.ExpiredSignatureError:
        raise "Token has expired."
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    
def get_user_details(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):

    print(token)
    user_data=validate_jwt_token(token=token)
    print("user_data",user_data)
    if "user_email" not in user_data:
        raise HTTPException(status_code=400,detail="Invalid Credentials")

    user_data_from_table=db.query(User).filter(User.email==user_data["user_email"]).first()
    print("user_data_from_table",user_data_from_table.id)
    return user_data_from_table