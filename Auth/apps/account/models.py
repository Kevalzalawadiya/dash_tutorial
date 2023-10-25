from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from config.settings import Base
from sqlalchemy.orm import relationship
from .models import ProjectDeveloper, Project





class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50),  nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    projects=relationship("Project", back_populates="user")
    projectdevelopers = relationship("ProjectDeveloper", back_populates="user")
    tasks = relationship("Tasks", back_populates="user")
    tasks_create = relationship("Tasks", back_populates="user_create")
    tasks_deleted_by = relationship("Tasks", back_populates="user_deleted_by")
    taskplanner = relationship("TaskPlanner", back_populates="user_name")


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=func.now())

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    email = Column(String, primary_key=True)
    reset_token = Column(String)
    reset_token_expiry = Column(DateTime)