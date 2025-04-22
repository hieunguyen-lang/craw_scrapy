FROM python:3.9-slim

# Cài đặt các dependencies cần thiết
RUN apt-get update && apt-get install -y cron



# Copy mã nguồn vào container
COPY . /app
WORKDIR /app
# Cài đặt dependencies
RUN pip install -r requirements.txt
# Copy cron job vào container
COPY cronjob /etc/cron.d/spider-cron

# Set quyền cho cron file
RUN chmod 0644 /etc/cron.d/spider-cron

# Đăng ký cron job
RUN crontab /etc/cron.d/spider-cron




# Chạy cron và Scrapy
CMD ["cron", "-f"]
