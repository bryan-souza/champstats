from pydantic import BaseModel, EmailStr
from typing import Optional
from beanie import Document, Indexed
from datetime import datetime, timedelta


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(UserUpdate):
    email: Indexed(EmailStr, unique=True)
    disabled: bool = False


class User(Document, UserOut):
    password: str
    email_confirmed_at: Optional[datetime] = None

    class Settings:
        name = 'users'


class AccessToken(BaseModel):
    access_token: str
    access_token_expires: timedelta = timedelta(minutes=15)


class RefreshToken(AccessToken):
    refresh_token: str
    refresh_token_expires: timedelta = timedelta(days=30)
