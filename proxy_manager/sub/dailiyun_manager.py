import settings

from proxy_manager.base_proxy_managers import BaseProxyManager


class DaiLiCloudProxyManager(BaseProxyManager):
    """
    http://www.dailiyun.com/
    """

    PROXY_URL = settings.DAI_LI_CLOUD

    def parse(self, html):
        self.proxies = list(filter(lambda x: x, html.split()))
        self.scores = [self.PROXY_MAX_USE_TIMES] * len(self.proxies)


def main():
    manager = DaiLiCloudProxyManager()
    print(manager.random())


if __name__ == '__main__':
    main()
