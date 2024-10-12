import sys
import scrapy
from scrapy.exceptions import CloseSpider, DontCloseSpider
from twisted.internet import reactor
from scrapy.selector import Selector

sys.path.append(r".\seCrawler\common")
from seCrawler.common.searResultPages import SearResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors


class KeywordSpider(scrapy.Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com', 'google.com', 'baidu.com']

    def __init__(self, keyword_file='keywords.txt', se='baidu', pages=5, max_retries=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword_file = keyword_file
        self.searchEngine = se.lower()
        self.pages = int(pages)
        self.max_retries = max_retries
        self.keywords = self.load_keywords()  # 读取关键词列表
        self.selector = SearchEngineResultSelectors.get(self.searchEngine, '')
        self.retry_count = 0
        self.timeout_limit = 60  # 设置超时时间为 60 秒

    def load_keywords(self):
        """从文件中读取所有关键词"""
        try:
            with open(self.keyword_file, 'r', encoding='utf-8') as f:
                return [line.strip().lower() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            self.logger.error(f"关键词文件 {self.keyword_file} 未找到。")
            return []

    def start_requests(self):
        """逐个关键词发起请求"""
        for keyword in self.keywords:
            # 获取每个关键词的分页 URL 列表
            page_urls = SearResultPages(keyword, self.searchEngine, self.pages)
            for url in page_urls:
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword})

    def parse(self, response):
        keyword = response.meta['keyword']
        self.logger.info(f"正在解析 URL: {response.url}，关键词: {keyword}")

        # 提取每个搜索引擎对应的搜索结果链接
        urls = Selector(response).xpath(self.selector).extract()
        if not urls:
            self.retry_count += 1
            if self.retry_count > self.max_retries:
                self.logger.warning(f"关键词 {keyword} 超过最大重试次数，跳过该关键词。")
                next_keyword = self.keywords[self.retry_count]  # 切换下一个关键词
                next_page_urls = SearResultPages(next_keyword, self.searchEngine, self.pages)

                for next_url in next_page_urls:
                    yield scrapy.Request(url=next_url, callback=self.parse, meta={'keyword': next_keyword})
            else:
                self.logger.warning(f"未能从 {response.url} 提取到任何结果，尝试使用下一个关键词。")
        else:
            self.retry_count = 0  # 重置重试计数
            # 输出每个结果链接及其对应的关键词
            for url in urls:
                yield {
                    'url': url,
                    'keyword': keyword
                }

    def get_next_keyword(self, current_keyword):
        """获取下一个关键词"""
        try:
            current_index = self.keywords.index(current_keyword)
            return self.keywords[current_index + 1] if current_index + 1 < len(self.keywords) else None
        except ValueError:
            return None

    def schedule_next_request(self):
        """安排下一个请求"""
        self.crawler.engine.pause()  # 暂停爬取
        reactor.callLater(self.timeout_limit, self.resume_crawl)  # 等待超时后继续爬取

    def resume_crawl(self):
        """恢复爬取"""
        self.crawler.engine.unpause()  # 恢复爬取
        raise DontCloseSpider
