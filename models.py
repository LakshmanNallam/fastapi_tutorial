from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password=Column(String,nullable=False, server_default='123')

    # ORM relationship
    posts=relationship("BlogPosts",back_populates="user")

class BlogPosts(Base):
    __tablename__ = "blogposts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    file_path=Column(String,nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ORM relationship
    user = relationship("User", back_populates="posts")


