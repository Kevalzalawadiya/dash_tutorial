from sqlalchemy import Column, Integer, String,Boolean, DateTime, func,ForeignKey
from sqlalchemy.orm import relationship
from config.settings import *
from apps.project.models import *

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    project=relationship("Project",back_populates="user_mangeby")
    # projectdevelopers=relationship("ProjectDeveloper",back_populates="users")
    # task=relationship("Task",back_populates="users")
    # task=relationship("Task",back_populates="users")
    # task=relationship("Task",back_populates="users")
    # taskplanner=relationship("TaskPlanner",back_populates="users")
    token = relationship("TokenTable", back_populates="user")
    passwordresettoken=relationship("PasswordResetToken",back_populates="user")
    



class TokenTable(Base):
    __tablename__ = "token"
    token_id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String(450),nullable=False)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship("User", back_populates="token")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    passwordresettoken_id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    reset_token = Column(String)
    reset_token_expiry = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user=relationship("User",back_populates="passwordresettoken")