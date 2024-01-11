from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class requestdetails(BaseModel):
    email:str
    password:str

class UserResponse(UserBase):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class TokenTableBase(BaseModel):
    access_token: str
    refresh_token: str
    status: bool

class changepassword(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
   

class TokenTableCreate(BaseModel):
    access_token: str
    refresh_token: str
    status: bool
    user_id: int  
    created_date: datetime
    
class TokenTableResponse(TokenTableCreate):
    token_id: int
    created_date: datetime
    user: UserResponse

    class Config:
        orm_mode = True

class PasswordResetTokenBase(BaseModel):
    email: EmailStr
    reset_token: str
    reset_token_expiry: datetime

class PasswordResetTokenCreate(PasswordResetTokenBase):
    pass  

class PasswordResetTokenResponse(PasswordResetTokenBase):
    passwordresettoken_id: int
    user: UserResponse

    class Config:
        orm_mode = True

class ResetPassword(BaseModel):
    token: str
    new_password: str
