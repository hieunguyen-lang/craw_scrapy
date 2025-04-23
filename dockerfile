FROM python:3.9-slim

# Cài đặt các dependencies cần thiết
RUN apt-get update && apt-get install -y cron



# Copy mã nguồn vào container
COPY . /app
WORKDIR /app/myproject
# Cài đặt dependencies
RUN pip install -r requirements.txt

RUN cd myproject
CMD ["scrapy", "crawl", "express_spider"]
