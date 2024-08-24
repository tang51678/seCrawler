# seCrawler（搜索引擎爬虫）

一个基于 Scrapy 的项目，用于爬取 Google/Bing/Baidu 搜索引擎的搜索结果。

`seCrawler` 是一个基于 Scrapy 的搜索引擎爬虫项目，支持 Bing、Google 和 Baidu 搜索引擎的关键词爬取。项目依赖于 Python 3.8 和 Scrapy 框架。

项目来源：  
[GitHub - xtt129/seCrawler](https://github.com/xtt129/seCrawler)  
[GitHub - Christings/seCrawler](https://github.com/Christings/seCrawler)

特别感谢分享！

# 本次优化地方如下:

## 优化点

1. **SQLite 数据库存储**：将爬取的数据存储在 `urls.sqlite3` 数据库中，相比传统的 TXT 文件存储，SQLite 提供了更高效的查询和数据管理能力。
2. **代码结构优化**：
   - 将核心功能模块化，分离了 `common` 和 `spiders` 目录中的逻辑，使得代码更加清晰和易于维护。
   - `common` 目录下包含了 `searchEngines.py` 和 `searResultPages.py`，处理不同搜索引擎和结果页面的逻辑。
   - `spiders` 目录下包含了主要的爬虫实现 `keywordSpider.py`，聚焦于具体的爬取任务。
3. **配置管理**：
   - 配置文件 `settings.py` 提供了灵活的爬虫设置，包括下载延迟、并发请求等，可以根据需要调整以防止 IP 封禁。

## 不同之处

- **SQLite 替代 TXT 文件**：相比于 TXT 文件，使用 SQLite 数据库提升了数据存储的可靠性和查询效率，减少了数据丢失和处理复杂性。
- **模块化设计**：与简单的爬虫项目不同，本项目将功能模块化，增强了可维护性和可扩展性。每个模块有明确的职责，代码更加清晰。
- **爬虫和搜索引擎的抽象**：`searchEngines.py` 负责不同搜索引擎的抽象和处理，使得添加新搜索引擎变得更加简便。
- **代理随机选择**：ProxyMiddleware 类实现了从代理列表中随机选择代理的功能，有助于提高爬取时的匿名性和灵活性。
- **动态加载用户代理**：RandomUserAgentMiddleware 类通过 load_user_agents 方法从 user_agents.txt 文件动态加载用户代理。这使得用户代理可以方便地进行更新而无需修改代码。

## 亮点

1. **灵活配置**：支持多种搜索引擎，通过参数配置即可轻松切换，不需要修改代码。
2. **扩展性强**：项目结构设计允许轻松扩展新的功能模块或支持新的搜索引擎。
3. **高效存储**：SQLite 数据库的使用使得数据存储和管理更加高效和可靠。

## 中文

本项目用于爬取 Bing、Google、Baidu 搜索引擎中的关键词搜索结果，基于 Python 3.8 和 Scrapy。

使用方法：
--- 进入项目目录后执行以下指令 ---

Bing：

```bash
scrapy crawl keywordSpider -a keyword=Spider-Man -a se=bing -a pages=50

scrapy crawl keywordSpider -a keyword="Spider-Man filetype:doc" -a se=bing -a pages=50
```

百度：

```bash
scrapy crawl keywordSpider -a keyword=Spider-Man -a se=baidu -a pages=50
```

Google：

```bash
scrapy crawl keywordSpider -a keyword=Spider-Man -a se=google -a pages=50
```

本项目没有 IP 保护功能，过度爬取可能会导致 IP 被封禁。可以尝试在 `settings.py` 文件中延长下载时间间隔来减轻封禁风险，例如：`DOWNLOAD_DELAY=10`。

## 文件结构

```
D:.
│  init_db.py
│  pipelines.py
│  settings.py
│  urls.sqlite3
│  __init__.py
│
├─common
│  │  searchEngines.py
│  │  searResultPages.py
│  │  __init__.py
│
├─spiders
│  │  keywordSpider.py
│  │  __init__.py
│
└─__pycache__
        pipelines.cpython-36.pyc
        pipelines.cpython-38.pyc
        settings.cpython-36.pyc
        settings.cpython-38.pyc
        __init__.cpython-36.pyc
        __init__.cpython-38.pyc
```
