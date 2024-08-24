from .searchEngines import SearchEngines

class SearResultPages:
    def __init__(self, keyword, searchEngine, totalPage):
        self.keyword = keyword
        self.searchEngine = searchEngine.lower()
        self.searchEngineUrl = SearchEngines[self.searchEngine]
        self.totalPage = totalPage
        self.currentPage = 0
        print(f"total page: {self.totalPage}")

    def __iter__(self):
        return self

    def _currentUrl(self):
        return self.searchEngineUrl.format(self.keyword, str(self.currentPage * 10))

    def __next__(self):
        if self.currentPage < self.totalPage:
            url = self._currentUrl()
            self.currentPage += 1
            return url
        raise StopIteration