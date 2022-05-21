import settings

from proxy_manager.base_proxy_managers import BaseProxyManager


class PaDaiLiProxyManager(BaseProxyManager):
    """
    http://www.padaili.com
    """

    PROXY_URL = settings.PA_DAI_LI_PROXY_URL

    def parse(self, html):
        self.proxies = list(filter(lambda x: x.strip(), html.split('<br/>')))
        self.scores = [self.PROXY_MAX_USE_TIMES] * len(self.proxies)


def main():
    manager = PaDaiLiProxyManager()
    print(manager.random())


if __name__ == '__main__':
    main()
