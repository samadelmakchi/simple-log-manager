# استفاده از تصویر رسمی Python
FROM python:3.10

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های پروژه
COPY requirements.txt .

# به‌روزرسانی فهرست بسته‌ها و نصب کلاینت PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن باقی فایل‌های پروژه
COPY . .

# باز کردن پورت برای اجرای API
EXPOSE 8000

# اجرای FastAPI با Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
