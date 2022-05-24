from urllib import parse
from generator.helper.job51_helper import Job51Helper
from generator.base_url_generator import BaseUrlGenerator


class Job51UrlGenerator(BaseUrlGenerator):
    """ 51job 网址生成器 """

    base_url = 'https://search.51job.com/list/'
    part_kw = '000000,000000,0000,00,9,99,{},2,'
    part_pn = '{}.html?lang=c&postchannel=0000&workyear=01&cotype=99&'
    part_dg = 'degreefrom={}&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='

    degree_map = {'本科': '04', '硕士': '05', '博士': '06'}

    settings_path = '/Users/luyan/Documents/PyCharm/zhouch/generator/settings/Job51UrlGenerator.gs'

    def __init__(self):
        super().__init__()
        self.exe_index = 0
        self.helper = Job51Helper(self.settings_path)
        self.progress_list = self.helper.progress_list

    def next(self):
        """ 返回下一类网址（例如专业或学位不同） """
        for i, item in enumerate(self.progress_list):
            if item[4]: continue
            self.exe_index = i
            yield self.next_page()

    def next_page(self):
        """ 返回同一专业学位下的下一页网址 """
        item = self.info()
        item[3] += 1
        return self._genurl()

    def info(self):
        """ 返回当前网址的信息 """
        return self.progress_list[self.exe_index]

    def _genurl(self):
        """ 生成 URL """
        kw, degree, _, pages, __ = self.info()
        degree = self.degree_map[degree]
        kw = parse.quote(kw).replace('%', '%25')
        return self.base_url + self.part_kw.format(kw) + self.part_pn.format(pages) + self.part_dg.format(degree)

    def update_settings(self):
        """ 更新配置文件 """
        self.helper.write_to_settings_file()
