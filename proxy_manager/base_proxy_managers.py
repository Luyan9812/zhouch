import requests

from loguru import logger
from retrying import retry
from random import randint
from settings import PROXY_TEST, PROXY_TEST_URL
from util_manager.json_manager import JsonManager


class BaseProxyManager(object):
    """ 代理类的基类 """

    # 代理商网址
    PROXY_URL = ''

    # 每个代理最多使用多少次
    PROXY_MAX_USE_TIMES = 50

    def __init__(self):
        self.scores = []
        self.proxies = []
        self.json_manager = JsonManager()

    @staticmethod
    def _gen(proxy):
        """ 根据代理ip和端口号生成代理字典 """
        return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}

    def _test(self, index):
        """ 测试代理是否可用 """
        if not PROXY_TEST: return True
        is_success = False
        try:
            proxies = self._gen(self.proxies[index])
            resp = requests.get(PROXY_TEST_URL, proxies=proxies)
            is_success = (resp.status_code == 200)
        finally:
            return is_success

    @retry(stop_max_attempt_number=3,
           retry_on_exception=lambda e: isinstance(e, requests.RequestException))
    def fetch(self):
        """ 获取代理信息，遇到请求异常就重试，最多重试 3 次 """
        logger.info(f'Get proxies: {self.PROXY_URL}')
        resp = requests.get(self.PROXY_URL)
        if resp.status_code != 200: raise requests.RequestException
        self.parse(resp.text)

    def random(self):
        """ 返回一个随机代理 """
        try:
            if not self.proxies: self.fetch()
            while self.proxies:
                index = randint(0, len(self.proxies) - 1)
                sub_score = 1 if self._test(index) else 10
                self.scores[index] -= sub_score
                proxy = self.proxies[index]
                if self.scores[index] <= 0:
                    del self.scores[index]
                    del self.proxies[index]
                if sub_score == 1: return self._gen(proxy)
                if not self.proxies: self.fetch()
        except requests.RequestException:
            logger.error('代理获取失败')

    def parse(self, html):
        raise NotImplementedError


def main():
    pass


if __name__ == '__main__':
    main()
