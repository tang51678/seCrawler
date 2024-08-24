# middlewares.py

import random

class ProxyMiddleware:
    def __init__(self):
        # 在这里填入你的代理列表
        self.proxies = [
            'http://proxy1.com',
            'http://proxy2.com',
            # 可以添加更多代理
        ]

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)

class RandomUserAgentMiddleware:
    def __init__(self):
        # 读取用户代理列表
        self.user_agents = self.load_user_agents()

    def load_user_agents(self):
        with open('user_agents.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
