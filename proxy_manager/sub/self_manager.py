from proxy_manager.base_proxy_managers import BaseProxyManager


class SelfProxyManager(BaseProxyManager):

    PROXY_URL = 'http://127.0.0.1:8848/random'

    def parse(self, html):
        self.proxies.append(html)
        self.scores.append(self.PROXY_MAX_USE_TIMES)


def main():
    manager = SelfProxyManager()
    print(manager.random())


if __name__ == '__main__':
    main()
