# Scrapy settings for seCrawler project

BOT_NAME = 'seCrawler'

SPIDER_MODULES = ['seCrawler.spiders']
NEWSPIDER_MODULE = 'seCrawler.spiders'

# 用户代理设置
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

# 控制爬取的深度
DEPTH_LIMIT = None

CLOSESPIDER_PAGECOUNT = None  # 或者删除该行
CLOSESPIDER_ITEMCOUNT = None  # 或者删除该行

DOWNLOAD_TIMEOUT = 15  # 设置超时为15秒
RETRY_TIMES = 3  # 尝试重试3次

CONCURRENT_REQUESTS = 32  # 增加并发请求数
DOWNLOAD_DELAY = 0.5  # 设置较短的下载延迟

DOWNLOAD_FAIL_ON_DATALOSS = False


# 配置 Item Pipeline
ITEM_PIPELINES = {
    'seCrawler.pipelines.SespiderPipeline': 1,
}

# 启用中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'seCrawler.middlewares.RandomUserAgentMiddleware': 400,
}

# 禁用代理相关中间件
