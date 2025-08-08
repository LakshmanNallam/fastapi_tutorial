from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine("postgresql://postgres:yourpassword@localhost:5432/fastapi") # handles the actual DB connection.

 # Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine) #is used for creating DB sessions.

Base = declarative_base() # Base is used to create model classes.

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()