import os
import re
import time

from loguru import logger
from domain.job import Job
from settings import JOB51_COOKIE
from analysis.job_analysis import JobWriter
from util_manager.json_manager import JsonManager
from spiders.base_requests_spider import BaseRequestsSpider
from generator.sub.job51_url_generator import Job51UrlGenerator


class Job51Spider(BaseRequestsSpider):
    """ 51job 爬虫 """

    ENCODING = 'gbk'

    def __init__(self):
        super().__init__()
        self.job_list = []
        self.cookie = JOB51_COOKIE
        self.job_writer = JobWriter()
        self.jmanager = JsonManager()
        self.generator = Job51UrlGenerator()
        self.root_path = '/Users/luyan/Downloads/zhouch/jobs'

    def next(self):
        """ 获取下一个要爬取的 URL """
        yield from self.generator.next()

    def parse(self, html):
        """ 解析获取的网页 """
        info = self.generator.info()
        logger.info(f'解析：{info[0]}-{info[1]}-{info[3]}')
        pattern = 'window.__SEARCH_RESULT__.*?({.*?})</script>'
        string = re.search(pattern, html).group(1)
        jobs = self.jmanager.load_s(string).get('engine_jds', [])
        if info[3] % 100 == 0: time.sleep(60)
        for job in jobs:
            company = job['company_name']
            location = job['workarea_text'].split('-')[0]
            job_name = job['job_name']
            salary = job['providesalary_text']
            yield Job.new_job(company, location, job_name, salary)
        if len(jobs) > 0:
            yield self.generator.next_page()
        else: self.update(True)

    def process_item(self, item):
        self.job_list.append(item)

    def update(self, finished=False):
        logger.info(f'updating')
        info = self.generator.info()
        info[3] -= 1
        info[-1] = finished
        info[2] += len(self.job_list)
        self.generator.update_settings()  # 更新配置文件
        excel_path = os.path.join(self.root_path, info[0], f'_{info[0]}.xlsx')
        self.job_writer.write_job(excel_path, info[1], self.job_list)
        self.job_writer.write_progress(excel_path, info[:])
        self.job_list.clear()


def main():
    spider = Job51Spider()
    spider.run()


if __name__ == '__main__':
    main()
