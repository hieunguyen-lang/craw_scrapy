import scrapy
from datetime import datetime
import re
from myproject.items import ArticleItem
from lxml import etree, html
from bs4 import BeautifulSoup
from myproject.rabbitmq_producer import RabbitMQClient
import json
class ExpressSpider(scrapy.Spider):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rabbitmq_client = RabbitMQClient()
        self.channel = self.rabbitmq_client.channel
        
        
    def get_config_for_url(self, url):
        """
        Lấy cấu hình từ settings.py dựa trên URL.
        Trả về cấu hình tương ứng với URL.
        """
        if 'https://vnexpress.net' in url:
            return self.settings.get('EXPRESS_SETTINGS')
        elif 'https://dantri.com.vn' in url:
            return self.settings.get('DAN_TRI_SETTINGS')
    def next_page(self, url,category,i):
        """
        Lấy cấu hình từ settings.py dựa trên URL.
        Trả về cấu hình tương ứng với URL.
        """
        if 'https://vnexpress.net' in url:
            return f"{category}-p{i + 1}"
        elif 'https://dantri.com.vn' in url:
            base = category.replace(".htm", "")
            url = f"{base}/trang-{i+1}.htm"
            return url
    name = "express_spider"
    allowed_domains = ["vnexpress.net","dantri.com.vn"]
    start_urls = [ 
                "https://dantri.com.vn/",
                "https://vnexpress.net/",
                #   "https://vnexpress.net/the-gioi",
                #   "https://vnexpress.net/kinh-doanh",
                #   "https://vnexpress.net/cong-nghe",
                #   "https://vnexpress.net/khoa-hoc",
                #   "https://vnexpress.net/bat-dong-san",
                #   "https://vnexpress.net/suc-khoe",
                #   "https://vnexpress.net/the-thao"
                  ]
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        'DUPEFILTER_DEBUG': True  # Giảm log hệ thống, giữ terminal sạch
    }
    def convert_to_datetime(self,date_str,url):
        
        if not date_str:
            return None  # Trả về None nếu date_str là None hoặc rỗng
        if 'https://vnexpress.net' in url:
            
            # Loại bỏ phần "Thứ bảy," và "(GMT+7)" trong chuỗi
            date_str = re.sub(r"^.*?,\s*(\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2})\s*\(GMT[+-]\d{1,2}\)$", r"\1", date_str)
            
            # Chuyển đổi thành datetime object
            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y, %H:%M")
                
                return date_obj.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
        if 'https://dantri.com.vn' in url:
            
            clean_date = date_str.split(", ")[1]  # "10/04/2025 - 05:57"
            try:
                # Chuyển về datetime
                dt = datetime.strptime(clean_date, "%d/%m/%Y - %H:%M")
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
              
    def get_category(self,html_content,satrt_urls):
        
        # Tìm kiếm các thẻ <meta> có thuộc tính property="article:section"
        category = html_content.xpath('.//*[@id="wrap-main-nav"]/nav/ul/li')
        list_category = []
        for item in category:
            # Lấy giá trị của thuộc tính content
            category_url = satrt_urls +item.xpath('.//a/@href').get()
            list_category.append(category_url)
            #category = item.xpath('.//meta[@property="article:section"]/@content').get()
        
        return list_category
    def get_article_category(self,response):
        #Lấy danh sách các article trong danh mục
        root = etree.fromstring(response.body)
        items = root.xpath('//item')
        print("🔍 Đang lấy danh sách bài viết:", len(items))
        if items:
            for item in items:
                    #Lấy các thông tin cần thiết từ từng bài viết
                    title_article = item.xpath('title/text()')[0]
                    link_article_detail = item.xpath('link/text()')[0]
                    raw_description = item.xpath('description/text()')[0]
                    # Xử lý CDATA và loại bỏ phần CDATA
                    clean_description = re.sub(r'<!\[CDATA\[|\]\]>', '', raw_description)
                    soup = BeautifulSoup(clean_description, 'html.parser')
                    description_article = soup.get_text()
                    # Lấy href của thẻ <a>
                    a_tag = soup.find('a')
                    image_url = a_tag['href'] if a_tag else None
                    
                    data_article_parent = {
                        'title': title_article,
                        'link': link_article_detail,
                        'description': description_article,
                        'image_url': image_url
                    }
                    data_article_parent.update(response.meta)
                    #print(data_article_parent['ARTICLE_AUTHOR_XPATH'])
                    #count +=1
                    #print("🔍 Trang này có bài viết:",link_article_detail,count)
                    #truy  cập vào chi tiết bài viết
                    if link_article_detail:
                        yield scrapy.Request(url= link_article_detail,
                                            meta=data_article_parent, 
                                            callback=self.parse_detail)
                    
        
    def parse(self, response):
        
        url_config = self.get_config_for_url(response.url)
        #truy cập danh sách các danh mục RSS
        for category in url_config['CATEGORY_URL']:
            
            yield scrapy.Request(url=category, callback=self.get_article_category,meta=url_config)
            
        
    def parse_detail(self, response):
        #lấy các thông tin chi tiêt bài viết
        item = ArticleItem()
        item['title'] = str(response.meta['title']).strip()
        item['description'] = response.meta['description']
        item['url'] = response.meta['link']
        item['author'] = response.xpath(response.meta['ARTICLE_AUTHOR_XPATH']).get()
        item['published_date'] = self.convert_to_datetime(str(response.xpath(response.meta['ARTICLE_PULISHED_DATE_XPATH']).get()).strip(),response.url)
        item['content'] = ' '.join(response.xpath('//article//p//text()').getall()).strip()
        item['tags'] = ', '.join(response.xpath(response.meta['ARTICLE_TAG_XPATH']).getall()).strip()
        item['image_url'] = response.meta['image_url']
        
        #Gửi message đến RabbitMQ
        self.rabbitmq_client.send_to_rabbitmq('data_crawled', dict(item))
        yield item

        # for product in response.css("div.product-item"):
        #     yield {
        #         'title': product.css("h3.product-title::text").get(),
        #         'price': product.css("span.price::text").get(),
        #         'link': response.urljoin(product.css("a::attr(href)").get()),
        #         'image': product.css("img::attr(src)").get()
        #     }
