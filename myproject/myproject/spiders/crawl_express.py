import scrapy
from datetime import datetime
import re
from myproject.items import ArticleItem
class ExpressSpider(scrapy.Spider):
    
    name = "express_spider"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net"
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
    def convert_to_datetime(self,date_str):
        if not date_str:
            return None  # Trả về None nếu date_str là None hoặc rỗng
        
        # Loại bỏ phần "Thứ bảy," và "(GMT+7)" trong chuỗi
        date_str = re.sub(r"^.*?,\s*(\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2})\s*\(GMT[+-]\d{1,2}\)$", r"\1", date_str)
        
        # Chuyển đổi thành datetime object
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y, %H:%M")
            return date_obj
        except ValueError:
            return None  # Trả về None nếu không thể chuyển đổi ngày  # Trả về None nếu không thể chuyển đổi ngày
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
        articles = response.xpath('//*[@id="automation_TV1"]/div/article')
            
        for article in articles:
            # print(article.xpath('.//h3[@class="title-news"]/a/text()').get())
            # print(article.xpath('.//a/@href').get())
            # print(article.xpath('.//p[@class="description"]/a/text()').get())
            title_article = article.xpath('.//h3[@class="title-news"]/a/text()').get()
            link_article_detail = article.xpath('.//a/@href').get()
            description_article = article.xpath('.//p[@class="description"]/a/text()').get()
            image_url = article.xpath('.//img/@data-src').get()
            data_article_parent = {
                'title': title_article,
                'link': link_article_detail,
                'description': description_article,
                'image_url': image_url
            }
            if link_article_detail:
                print("🔍 Đang lấy link:", link_article_detail)
                yield response.follow(link_article_detail,
                                      meta=data_article_parent, 
                                      callback=self.parse_detail)
    def parse(self, response):
        html_content = response.body
        print("🔍 Đang xử lý:", response.url)
        #lấy category của trang
        categorys = self.get_category(response,str(response.url))
        print("🔍 Danh sách category:", categorys)
        #self.log("HTML content saved to output.html")
        for category in categorys:
            yield scrapy.Request(url=category, callback=self.get_article_category)
        
    def parse_detail(self, response):
        # with open("output.html",  "w", encoding="utf-8") as f:
        #     # for article in articles:
        #     #     html = article.get()
        #     #     f.write(html + "\n\n")
        #     f.write(response.body.decode("utf-8") + "\n\n")
        # print("🔍 Đang lấy detail:", response.url)
        #print(response.xpath('//div[contains(@class, "header-content") and contains(@class, "width_common")]//span[@class="date"]//text()').get())
        #print(response.xpath('//div[contains(@class,"sidebar-1 pin-comment")]div//h4//text()').getall())
        item = ArticleItem()
        item['title'] = response.meta['title']
        item['description'] = response.meta['description']
        item['url'] = response.meta['link']
        item['author'] = response.xpath('//article//p//strong//text()').get()
        item['published_date'] = self.convert_to_datetime(response.xpath('//div[contains(@class, "header-content") and contains(@class, "width_common")]//span[@class="date"]//text()').get())
        item['content'] = ' '.join(response.xpath('//article//p//text()').getall()).strip()
        item['tags'] = ''.join(response.xpath('//div[contains(@class,"tags")]//h4//text()').getall()).strip()
        item['image_url'] = response.meta['image_url']
        yield item

        # for product in response.css("div.product-item"):
        #     yield {
        #         'title': product.css("h3.product-title::text").get(),
        #         'price': product.css("span.price::text").get(),
        #         'link': response.urljoin(product.css("a::attr(href)").get()),
        #         'image': product.css("img::attr(src)").get()
        #     }
