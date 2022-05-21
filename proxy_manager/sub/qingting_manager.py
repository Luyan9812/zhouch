import json
import settings

from loguru import logger
from proxy_manager.base_proxy_managers import BaseProxyManager


class QingTingProxyManager(BaseProxyManager):
    """
    https://proxy.horocn.com/
    """

    PROXY_URL = settings.QING_TING

    def parse(self, html):
        try:
            data = self.json_manager.load_s(html)['data']
            self.proxies = list(map(lambda x: f'{x["host"]}:{x["port"]}', data))
            self.scores = [self.PROXY_MAX_USE_TIMES] * len(self.proxies)
        except json.JSONDecodeError or KeyError:
            logger.error('QingTingProxyManager Parse Error')


def main():
    manager = QingTingProxyManager()
    print(manager.random())


if __name__ == '__main__':
    main()
