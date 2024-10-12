import os
import random
import logging


class RandomUserAgentMiddleware:
    def __init__(self):
        """
        初始化用户代理中间件，加载用户代理列表。
        """
        self.user_agents = self.load_user_agents()

    def load_user_agents(self):
        """
        从 user_agents.txt 文件中加载用户代理。
        :return: 用户代理列表
        """
        # 获取 user_agents.txt 文件的绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        user_agents_file = os.path.join(base_dir, 'user_agents.txt')

        try:
            with open(user_agents_file, 'r') as file:
                user_agents = [line.strip() for line in file if line.strip()]

            if not user_agents:
                logging.warning("用户代理列表为空，使用默认用户代理。")
            return user_agents
        except FileNotFoundError:
            logging.error(f"未找到 '{user_agents_file}' 文件，使用默认用户代理。")
            return []

    def process_request(self, request, spider):
        """
        为每个请求随机选择一个用户代理。
        :param request: 当前请求对象
        :param spider: 当前爬虫对象
        """
        if self.user_agents:
            user_agent = random.choice(self.user_agents)
            request.headers['User-Agent'] = user_agent
            logging.info(f"使用用户代理: {user_agent}")
        else:
            logging.warning("无可用用户代理，使用默认用户代理。")
