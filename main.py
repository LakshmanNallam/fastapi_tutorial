from fastapi import FastAPI, Depends, HTTPException
from database import engine , get_db
from models import *
from routers import user,blogposts,auth
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)  # Create tables # this Base is coming from the models.py file # we didn't expilicity exported it but it worked

origins = [
    "https://www.google.com"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router,tags=['user'])
app.include_router(blogposts.router,tags=['blogposts'])
app.include_router(auth.router,tags=['auth'])