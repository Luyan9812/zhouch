import re
import os

from util_manager.xlsx_manager import XlsxManager
from util_manager.list_manager import ListManager
from util_manager.file_manager import FileManager


class JobWriter(object):
    """ 将职位信息写进 xlsx 工作薄里 """

    def __init__(self):
        self.xmanager = XlsxManager()
        self.progress_sheetname = 'progress'

    @staticmethod
    def headers_job():
        """ 职位表表头信息 """
        return ['公司', '地区', '职位名称', '最低薪资', '最高薪资']

    @staticmethod
    def headers_progress():
        """ 进度表表头信息 """
        return ['专业', '学位', '已爬取数据条数', '已爬取数据页数', '是否爬取结束']

    def get_sheetnames(self):
        """ xlsx 工作薄 sheet 表的名字 """
        return ['本科', '硕士', '博士', self.progress_sheetname]

    def write_job(self, excel_path, sheetname, data):
        """ 往 xlsx 工作薄里写入职位数据 """
        data = list(map(lambda x: x.__dict__.values(), data))
        if not os.path.exists(excel_path):
            self.xmanager.init(excel_path, self.get_sheetnames(), create=True)
        self.xmanager.switch(excel_path, sheetname, create=False)
        if self.xmanager.empty():
            self.xmanager.write_line(1, self.headers_job())
        self.xmanager.append_lines(data)

    def write_progress(self, excel_path, data):
        """ 往 xlsx 工作薄里写入爬取进度 """
        if not os.path.exists(excel_path):
            self.xmanager.init(excel_path, self.get_sheetnames(), create=True)
        self.xmanager.switch(excel_path, self.progress_sheetname, create=False)
        if self.xmanager.empty():
            self.xmanager.write_line(1, self.headers_progress())
        lines = self.xmanager.read(start='A2')
        index = ListManager.find(lines, data, key=lambda x: x[1])
        if index < 0:
            lines.append(data)
        else:
            lines[index] = data
        self.xmanager.write_lines(2, lines)


class JobDistincter(object):
    """ 去重类。负责将爬取下来的数据按照公司、职位名称作为标准去重并写进新 xlsx 文件里 """

    def __init__(self):
        self.xmanager = XlsxManager()
        self.root_path = '/Users/luyan/Downloads/zhouch/jobs'

    @staticmethod
    def headers():
        """ 返回表头信息 """
        return ['公司', '地区', '职位名称', '最低薪资', '最高薪资']

    def _distinct_and_write_sheet(self, from_excel_path, to_excel_path, sheetname):
        """ 对某一个 sheet 去重并将结果写进另一个工作薄里 """
        self.xmanager.switch(from_excel_path, sheetname)
        data = ListManager.distinct(self.xmanager.read(start='A2'), key=lambda x: f'{x[0]}_{x[1]}_{x[2]}')
        self.xmanager.switch(to_excel_path, sheetname)
        self.xmanager.write_line(1, self.headers())
        self.xmanager.append_lines(data)

    def distinct_one(self, from_excel_path, to_excel_path=None):
        """ 解析一个 xlsx 文件 """
        if not to_excel_path:
            dirpath, filename = os.path.split(from_excel_path)
            subject = re.match('_(.*?)\.xlsx', filename).group(1)
            to_excel_path = os.path.join(dirpath, f'{subject}.xlsx')
        self.xmanager.init(to_excel_path, ['本科', '硕士', '博士'], create=True)
        self._distinct_and_write_sheet(from_excel_path, to_excel_path, '本科')
        self._distinct_and_write_sheet(from_excel_path, to_excel_path, '硕士')
        self._distinct_and_write_sheet(from_excel_path, to_excel_path, '博士')

    def distinct_many(self, excel_path_pairs):
        """ 解析多个 xlsx 文件 """
        for pair in excel_path_pairs:
            if isinstance(pair, (list, tuple)):
                self.distinct_one(*pair)
            else:
                self.distinct_one(pair, to_excel_path=None)

    def distinct_root(self, root_path=None):
        """ 给定文件根目录（zhouch/jobs），解析其下所有专业下所有 xlsx 文件 """
        if not root_path: root_path = self.root_path
        for dirpath in FileManager.list_sub_dirs(root_path, need_fullpath=True):
            for filepath in FileManager.list_sub_files(dirpath, pattern='_.*?\.xlsx', need_fullpath=True):
                self.distinct_one(filepath, to_excel_path=None)


class JobAnalyser1(object):
    """ 统计类1。根据爬取的数据做统计并将结果写进新 xlsx 文件里，表结构看 header() """

    def __init__(self):
        self.xmanager = XlsxManager()
        self.analyse_filename = '汇总.xlsx'
        self.analyse_sheetname = '汇总'
        self.root_path = '/Users/luyan/Downloads/zhouch/jobs'

    @staticmethod
    def headers():
        """ 返回统计表的表头信息 """
        return ['专业', '本科学历', '招聘企业数', '招聘岗位数', '平均工资',
                '硕士学历', '招聘企业数', '招聘岗位数', '平均工资',
                '博士学历', '招聘企业数', '招聘岗位数', '平均工资']

    @staticmethod
    def _sort_results_by_job_numbers(results: list):
        """ 按岗位数量对结果排序 """
        results.sort(key=lambda x: x[3] + x[7] + x[11], reverse=True)

    @staticmethod
    def _sort_results_by_avg_salary(results: list):
        """ 按照各学位平均工资和对结果排序 """
        results.sort(key=lambda x: x[4] + x[8] + x[12], reverse=True)

    def _write_analyse_results(self, to_excel_path, results):
        """ 将统计结果写进 xlsx 文件里 """
        self.xmanager.init(to_excel_path, [self.analyse_sheetname], create=True)
        self.xmanager.write_line(1, self.headers())
        self._sort_results_by_job_numbers(results)
        self.xmanager.append_lines(results)

    def _analyse_sheet(self, excel_path, sheetname):
        """ 返回一个工作表的统计结果 """
        self.xmanager.switch(excel_path, sheetname)
        origin_data = self.xmanager.read(start='A2')
        avg_salary = 0
        job_numbers = len(origin_data)
        company_numbers = len(ListManager.distinct(origin_data, key=lambda x: x[0]))
        for item in origin_data:
            avg_salary += (item[3] + item[4])
        if len(origin_data) > 0: avg_salary /= (2 * len(origin_data))
        return [sheetname, company_numbers, job_numbers, round(avg_salary, 2)]

    def _analyse_book(self, excel_path):
        """ 返回一个 xlsx 工作薄统计结果 """
        _, filename = os.path.split(excel_path)
        results = [filename.split('.', 1)[0]]
        results.extend(self._analyse_sheet(excel_path, '本科'))
        results.extend(self._analyse_sheet(excel_path, '硕士'))
        results.extend(self._analyse_sheet(excel_path, '博士'))
        return results

    def analyse_one(self, from_excel_path, to_excel_path=None):
        """ 统计一个 xlsx 工作薄 """
        results = []
        if not to_excel_path:
            to_excel_path = os.path.join(self.root_path, self.analyse_filename)
        results.append(self._analyse_book(from_excel_path))
        self._write_analyse_results(to_excel_path, results)

    def analyse_many(self, excel_paths, to_excel_path=None):
        """ 统计一些 xlsx 工作薄 """
        results = []
        if not to_excel_path:
            to_excel_path = os.path.join(self.root_path, self.analyse_filename)
        for path in excel_paths:
            results.append(self._analyse_book(path))
        self._write_analyse_results(to_excel_path, results)

    def analyse_root(self, root_path=None, to_excel_path=None):
        """ 给定文件根目录（zhouch/jobs），统计其下所有专业下所有 xlsx 工作薄 """
        results = []
        if not to_excel_path:
            to_excel_path = os.path.join(self.root_path, self.analyse_filename)
        if not root_path: root_path = self.root_path
        for dirpath in FileManager.list_sub_dirs(root_path, need_fullpath=True):
            for filepath in FileManager.list_sub_files(dirpath, pattern='[^_].*?\.xlsx', need_fullpath=True):
                results.append(self._analyse_book(filepath))
        self._write_analyse_results(to_excel_path, results)


def main():
    ja = JobAnalyser1()
    ja.analyse_root()


if __name__ == '__main__':
    main()
