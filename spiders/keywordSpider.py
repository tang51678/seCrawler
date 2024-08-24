import sys
sys.path.append(r".\seCrawler\seCrawler\common")

from scrapy.spiders import Spider
from seCrawler.common.searResultPages import SearResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import Selector

class KeywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com', 'google.com', 'baidu.com']

    def __init__(self, keyword, se='bing', pages=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors.get(self.searchEngine, '')
        pageUrls = SearResultPages(keyword, se, int(pages))
        self.start_urls = pageUrls

    def parse(self, response):
        self.logger.info(f"正在解析 URL: {response.url}")
        urls = Selector(response).xpath(self.selector).extract()
        for url in urls:
            yield {'url': url, 'keyword': self.keyword}
