# Scrapy settings for myproject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "myproject"

SPIDER_MODULES = ["myproject.spiders"]
NEWSPIDER_MODULE = "myproject.spiders"
# Cấu hình kết nối MySQL
MYSQL_HOST = 'mysql'  # Thay đổi thành địa chỉ của máy chủ MySQL
MYSQL_DB = 'crawl_data_express'
MYSQL_USER = 'hieunk'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = 3306
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "myproject (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
EXPRESS_SETTINGS = {
                        "CATEGORY_URL": [ 
                                        'https://vnexpress.net/rss/tin-tuc-24h.rss', 
                                        'https://vnexpress.net/rss/thoi-su.rss', 
                                        'https://vnexpress.net/rss/the-gioi.rss', 
                                        'https://vnexpress.net/rss/kinh-doanh.rss', 
                                        'https://vnexpress.net/rss/khoa-hoc-cong-nghe.rss', 
                                        'https://vnexpress.net/rss/goc-nhin.rss', 
                                        'https://vnexpress.net/rss/bat-dong-san.rss', 
                                        'https://vnexpress.net/rss/suc-khoe.rss', 
                                        'https://vnexpress.net/rss/the-thao.rss', 
                                        'https://vnexpress.net/rss/giai-tri.rss', 
                                        'https://vnexpress.net/rss/phap-luat.rss', 
                                        'https://vnexpress.net/rss/giao-duc.rss', 
                                        'https://vnexpress.net/rss/doi-song.rss', 
                                        'https://vnexpress.net/rss/oto-xe-may.rss', 
                                        'https://vnexpress.net/rss/du-lich.rss', 
                                        'https://vnexpress.net/rss/y-kien.rss', 
                                        'https://vnexpress.net/rss/tam-su.rss'],
                        "ARTICLE_XPATH": '//div[contains(@class,"width_common") and contains(@class, "list-news-subfolder")]//article[@class="item-news item-news-common thumb-left"]',
                        "ARTICLE_TITLE_XPATH": './/h3[@class="title-news"]/a/text()',
                        "ARTICLE_LINK_XPATH": './/a/@href',
                        "ARTICLE_DESCRIPTION_XPATH": './/p[@class="description"]/a/text()',
                        "ARTICLE_IMAGE_URL_XPATH": './/img/@data-src',
                        "ARTICLE_AUTHOR_XPATH": '//article//p//strong//text()',
                        "ARTICLE_PULISHED_DATE_XPATH": '//div[contains(@class, "header-content") and contains(@class, "width_common")]//span[@class="date"]//text()',
                        "ARTICLE_CONTENT_XPATH": '//article//p//text()',
                        "ARTICLE_TAG_XPATH": '//div[@class="tags"]/h4[@class="item-tag"]/a/text()',
                    }
DAN_TRI_SETTINGS  = {
                        "CATEGORY_URL": [    'https://dantri.com.vn/rss/kinh-doanh.rss', 
                                             'https://dantri.com.vn/rss/xa-hoi.rss', 
                                             'https://dantri.com.vn/rss/the-gioi.rss', 
                                             'https://dantri.com.vn/rss/giai-tri.rss', 
                                             'https://dantri.com.vn/rss/bat-dong-san.rss', 
                                             'https://dantri.com.vn/rss/the-thao.rss', 
                                             'https://dantri.com.vn/rss/suc-khoe.rss', 
                                             'https://dantri.com.vn/rss/noi-vu.rss', 
                                             'https://dantri.com.vn/rss/o-to-xe-may.rss', 
                                             'https://dantri.com.vn/rss/cong-nghe.rss', 
                                             'https://dantri.com.vn/rss/giao-duc.rss', 
                                             'https://dantri.com.vn/rss/lao-dong-viec-lam.rss', 
                                             'https://dantri.com.vn/rss/phap-luat.rss' 
                                             ],
                        "ARTICLE_XPATH": '//div[contains(@class,"article list")]//article[contains(@class,"article-item")]',
                        "ARTICLE_TITLE_XPATH": './/div[contains(@class,"article-content")]//h3[@class="article-title"]/a/text()',
                        "ARTICLE_LINK_XPATH": './/div[contains(@class,"article-content")]//h3[@class="article-title"]/a/@href',
                        "ARTICLE_DESCRIPTION_XPATH": './/div[contains(@class,"article-excerpt")]/a/text()',
                        "ARTICLE_IMAGE_URL_XPATH": './/img/@data-src',
                        "ARTICLE_AUTHOR_XPATH": '//article//div//div//div//text()',
                        "ARTICLE_PULISHED_DATE_XPATH": '//article//div//div//time//text()',
                        "ARTICLE_CONTENT_XPATH": '//article//p//text()',
                        "ARTICLE_TAG_XPATH": '//ul[@class="tags-wrap mt-30"]//li//a/text()',
                    }
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "myproject.middlewares.MyprojectSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "myproject.middlewares.MyprojectDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "myproject.pipelines.MySQLPipeline": 1,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
