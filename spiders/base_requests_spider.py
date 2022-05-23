import requests
import retrying

from loguru import logger
from retrying import retry
from fake_useragent import UserAgent


class BaseRequestsSpider(object):
    """ 使用requests请求的基类 """

    def __init__(self):
        self.cookie = ''
        self.ua = UserAgent()
        self.proxy_manager = None

    def get_request_headers(self):
        """ 获取请求头 """
        headers = {'User-Agent': self.ua.random}
        if self.cookie:
            headers['Cookie'] = self.cookie
        return headers

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)
    def fetch(self, url, proxies=None):
        """ 获取指定 URL 的内容 """
        try:
            logger.info(f'Begin fetch {url}')
            resp = requests.get(url, headers=self.get_request_headers(), proxies=proxies)
            if resp.status_code == 200: return resp.text
        except requests.RequestException:
            return None

    def next(self):
        """ 获取下一个要爬取的 URL """
        raise NotImplementedError

    def parse(self, html):
        """ 解析获取到的网页内容，返回处理结果和下一个要爬取的 URL """
        raise NotImplementedError

    def process_item(self, item):
        """ 处理爬取的对象 """
        raise NotImplementedError

    def on_close(self):
        """ 爬取结束的时候调用 """

    def _process(self, url, proxies=None):
        """ 爬取函数 """
        try:
            html = self.fetch(url, proxies=proxies)
            for item in self.parse(html):
                if item is str: return item
                else: self.process_item(item)
        except retrying.RetryError:
            logger.error(f'Error: {url}')

    def run(self, use_proxy=False):
        """ 入口函数 """
        try:
            for url in self.next():
                while url:
                    proxies = self.proxy_manager.random() if use_proxy else None
                    url = self._process(url, proxies=proxies)
        except Exception as e:
            logger.error(e)
        finally:
            self.on_close()
