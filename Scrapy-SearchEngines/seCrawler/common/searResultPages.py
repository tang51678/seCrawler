from .searchEngines import SearchEngines

class SearResultPages:
    def __init__(self, keyword, searchEngine, totalPage=None):
        self.keyword = keyword
        self.searchEngine = searchEngine.lower()
        self.searchEngineUrl = SearchEngines[self.searchEngine]
        self.totalPage = totalPage  # 允许 totalPage 为 None
        self.currentPage = 0
        self.has_more = True  # 用于记录是否还有更多结果
        print(f"total page: {self.totalPage}")

    def __iter__(self):
        return self

    def _currentUrl(self):
        return self.searchEngineUrl.format(self.keyword, str(self.currentPage * 10))

    def __next__(self):
        if self.totalPage is not None:
            if self.currentPage < self.totalPage:
                url = self._currentUrl()
                self.currentPage += 1
                return url
            raise StopIteration
        else:
            if self.has_more:  # 如果还有更多结果，就继续爬取
                url = self._currentUrl()
                self.currentPage += 1
                return url
            raise StopIteration

    def no_more_results(self):
        """当确认没有更多结果时调用此方法"""
        self.has_more = False
