from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import jwt
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import User, Log

# تنظیمات FastAPI
app = FastAPI()

# تنظیمات JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# تنظیمات پیکربندی رمزنگاری
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# تنظیمات SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql://log_user:log_password@db:5432/log_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# مدل Pydantic برای لاگ‌ها (برای پاسخ‌دهی)
class LogBase(BaseModel):
    microservice: str
    datetime: datetime
    message: str
    url: str
    idu: int

    class Config:
        orm_mode = True  # این تنظیم به FastAPI می‌گوید که از مدل SQLAlchemy داده‌ها را دریافت کند

# مدل SQLAlchemy برای لاگ‌ها (برای تعامل با دیتابیس)
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    microservice = Column(String)
    datetime = Column(DateTime, default=datetime.utcnow)
    message = Column(String)
    url = Column(String)
    idu = Column(Integer)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # یا آدرس‌های خاصی که به درخواست‌ها دسترسی دارند
    allow_credentials=True,
    allow_methods=["*"],  # یا فقط متدهای خاص مثل GET, POST
    allow_headers=["*"],  # یا فقط هدرهای خاص
)

# اتصال به دیتابیس و ایجاد جداول
Base.metadata.create_all(bind=engine)

# توابع مربوط به احراز هویت
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="توکن نامعتبر است")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="توکن منقضی شده است")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="توکن نامعتبر است")

    # پیدا کردن کاربر در پایگاه داده
    db = SessionLocal()
    user = get_user(db, username)
    db.close()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="کاربر یافت نشد")
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ثبت لاگ
@app.post("/logs")
def save_log(log: LogBase, token: str = Depends(oauth2_scheme)):
    verify_token(token)  # بررسی توکن
    db = SessionLocal()
    log_db = Log(**log.dict())  # استفاده از مدل Pydantic برای ثبت در دیتابیس
    db.add(log_db)
    db.commit()
    db.refresh(log_db)
    db.close()
    return {"status": "لاگ با موفقیت ذخیره شد"}

# گرفتن لیست لاگ‌ها
@app.get("/logs", response_model=List[LogBase])
def get_logs(token: str = Depends(oauth2_scheme)):
    verify_token(token)  # بررسی توکن
    db = SessionLocal()
    logs = db.query(Log).order_by(Log.datetime.desc()).all()
    db.close()
    return logs

# لاگین و دریافت توکن
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = get_user(db=db, username=form_data.username)
    db.close()
    print(f"verify_password: {verify_password(form_data.password, user.hashed_password)}")
    if user is None or not verify_password(form_data.password, user.hashed_password):
        print(f"User pass and Hash pass: {form_data.password}, {user.hashed_password}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="نام کاربری یا رمز عبور اشتباه است")
    
    # ایجاد توکن دسترسی
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# $2b$12$WqDpi5vQH5JhHv8uUuYZlOPbOoe3De4D.NB6AziA7XEjwvjKxr4I6  db
# $2b$12$WqDpi5vQH5JhHv8uUuYZlOPbOoe3De4D.NB6AziA7XEjwvjKxr4I6