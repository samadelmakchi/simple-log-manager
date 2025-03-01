# مرحله بیلد (Build Stage)
FROM node:22 AS build

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های ضروری
COPY package.json package-lock.json ./

# نصب وابستگی‌ها
RUN npm install

# کپی کردن باقی فایل‌های پروژه
COPY . .

# بیلد پروژه React
RUN npm run build

# مرحله اجرا (Run Stage) با Nginx
FROM nginx:alpine

# کپی فایل‌های بیلد شده به مسیر Nginx
COPY --from=build /app/build /usr/share/nginx/html

# کپی تنظیمات Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# باز کردن پورت 80
EXPOSE 80

# اجرای Nginx
CMD ["nginx", "-g", "daemon off;"]
