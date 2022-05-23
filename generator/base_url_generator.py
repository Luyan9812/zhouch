class BaseUrlGenerator(object):
    """ URL 生成器基类 """

    # 配置文件的路径
    settings_path = ''

    def next(self):
        """ 返回下一个网址 """
        raise NotImplementedError

    def info(self):
        """ 返回当前网址的基本信息 """
        raise NotImplementedError

    def update_settings(self):
        """ 更新配置文件信息 """
        pass
