import json
import settings

from loguru import logger
from proxy_manager.base_proxy_managers import BaseProxyManager


class IP3366ProxyManager(BaseProxyManager):
    """
    http://www.ip3366.net/
    """

    PROXY_URL = settings.IP3366

    def parse(self, html):
        try:
            self.proxies = self.json_manager.load_s(html, map_=lambda x: f'{x["Ip"]}:{x["Port"]}')
            self.scores = [self.PROXY_MAX_USE_TIMES] * len(self.proxies)
        except json.JSONDecodeError:
            logger.error('IP3366ProxyManager Parse Error')


def main():
    manager = IP3366ProxyManager()
    print(manager.random())


if __name__ == '__main__':
    main()
