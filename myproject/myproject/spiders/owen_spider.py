import scrapy

class OwenSpider(scrapy.Spider):
    name = "owen_spider"
    allowed_domains = ["owen.vn"]
    start_urls = ["https://owen.vn/"]

    def parse(self, response):
        for product in response.css("div.product-item"):
            yield {
                'title': product.css("h3.product-title::text").get(),
                'price': product.css("span.price::text").get(),
                'link': response.urljoin(product.css("a::attr(href)").get()),
                'image': product.css("img::attr(src)").get()
            }
