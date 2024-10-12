# -*- coding: utf-8 -*-
import sqlite3
from scrapy.exceptions import DropItem
import logging


class SespiderPipeline(object):
    def __init__(self):
        # 连接到 SQLite 数据库
        self.conn = sqlite3.connect('urls.sqlite3')
        self.c = self.conn.cursor()
        # 确保表存在
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                url TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            # 插入 URL 和 keyword 到数据库，忽略重复的 URL
            self.c.execute('INSERT OR IGNORE INTO urls (keyword, url) VALUES (?, ?)',
                           (item['keyword'], item['url']))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e}")
            raise DropItem(f"Failed to insert item {item}")
        return item

    def close_spider(self, spider):
        # 关闭数据库连接
        self.conn.close()
