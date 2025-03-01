from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()

# مدل Pydantic برای Log (ورودی/خروجی)
class Log(BaseModel):
    id: int
    log_message: str
    created_at: datetime

    class Config:
        orm_mode = True  # این برای تبدیل مدل SQLAlchemy به Pydantic است

# مدل SQLAlchemy برای Log
class LogDB(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    log_message = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# مدل Pydantic برای ورود کاربر
class UserLogin(BaseModel):
    username: str
    password: str

# مدل Pydantic برای پاسخ کاربر (بعد از ورود)
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True  # برای تبدیل از SQLAlchemy به Pydantic

# مدل SQLAlchemy برای User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)
    
