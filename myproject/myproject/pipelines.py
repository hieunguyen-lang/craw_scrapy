# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy.exceptions import DropItem

class MyprojectPipeline:
    def process_item(self, item, spider):
        return item


# class MySQLPipeline:
#     def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password,mysql_port):
#         self.mysql_host = mysql_host
#         self.mysql_db = mysql_db
#         self.mysql_user = mysql_user
#         self.mysql_password = mysql_password
#         self.mysql_port = mysql_port
#         self.conn = None
#         self.cursor = None

#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         return cls(
#             mysql_host=crawler.settings.get('MYSQL_HOST'),
#             mysql_db=crawler.settings.get('MYSQL_DB'),
#             mysql_user=crawler.settings.get('MYSQL_USER'),
#             mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
#             mysql_port=crawler.settings.get('MYSQL_PORT', 3306),
#         )

#     def open_spider(self, spider):
#         # Kết nối tới cơ sở dữ liệu MySQL khi spider được mở
#         self.conn = pymysql.connect(
#             host=self.mysql_host,
#             user=self.mysql_user,
#             password=self.mysql_password,
#             database=self.mysql_db,
#             port=self.mysql_port,
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         self.cursor = self.conn.cursor()

#     def close_spider(self, spider):
#         # Đóng kết nối khi spider kết thúc
#         self.conn.commit()
#         self.conn.close()

#     def process_item(self, item, spider):
#         # Đoạn code lưu item vào MySQL
#         sql = "INSERT INTO articles (title, description,content,author,published_date,tags,image_url,url) VALUES (%s, %s,%s, %s, %s,%s,%s,%s)"
#         values = (item['title'], item['description'],item['content'],item['author'],item['published_date'],item['tags'],item['image_url'],item['url'])  # Giả sử bạn có các trường 'field1', 'field2'
#         try:
#             self.cursor.execute(sql, values)
#             self.conn.commit()  # ✅ Commit ngay
#         except pymysql.MySQLError as e:
#             spider.logger.error(f"MySQL error: {e}")
#             raise DropItem(f"Error inserting item into MySQL: {item}")
#         return item
