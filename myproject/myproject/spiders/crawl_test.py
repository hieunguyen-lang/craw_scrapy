import scrapy

class HtmlSpider(scrapy.Spider):
    name = "html_spider"
    start_urls = [
        'https://owen.vn/',  # Replace with the URL you want to crawl
    ]

    def parse(self, response):
        # Extract the HTML content
        html_content = response.body
        # Save the HTML content to a file
        with open("output.html", "wb") as f:
            f.write(html_content)
        #self.log("HTML content saved to output.html")
        # Ensure the Scrapy project is properly set up and run this spider using the Scrapy command:
        # scrapy runspider /c:/Users/hieunk/Documents/hieunk-project/test.py



class BlogSpider(scrapy.Spider):
    name = 'blog'
    start_urls = ['https://example-blog.com']

    def parse(self, response):
        for post in response.css('div.post'):
            yield {
                'title': post.css('h2.title::text').get(),
                'link': post.css('a::attr(href)').get()
            }
