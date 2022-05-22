import os
import shutil

from loguru import logger
from functools import reduce
from util_manager.json_manager import JsonManager
from util_manager.xlsx_manager import XlsxManager
from util_manager.list_manager import ListManager


class JobAnalysis(object):
    """ 统计职位信息的操作类 """

    ROOT_PATH = '/Users/luyan/Downloads/zhouch/jobs'

    def __init__(self):
        self.analyse_data = []
        self.sorted_areas = []
        self.sorted_subjects = []
        self.areas_job_numbers = {}
        self.json_manager = JsonManager()
        self.xlsx_manager = XlsxManager()
        self.list_manager = ListManager()

    def move(self, target_dir):
        """ 将生成的职位 xlsx 文件复制一份到指定目录下 """
        os.path.exists(target_dir) or os.makedirs(target_dir)
        for dirname in os.listdir(self.ROOT_PATH):
            dirpath = os.path.join(self.ROOT_PATH, dirname)
            if not os.path.isdir(dirpath): continue
            for filename in os.listdir(dirpath):
                filepath = os.path.join(dirpath, filename)
                if not filename.endswith('.xlsx'): continue
                shutil.copy(filepath, os.path.join(target_dir, filename))

    @staticmethod
    def _get_degree(filename):
        """ 获取一个文件对应的学位是什么 """
        if '本科' in filename: return '本科'
        if '硕士' in filename: return '硕士'
        if '博士' in filename: return '博士'

    @staticmethod
    def _get_degree_level(degree):
        """ 获取一个学位对应的排序值 """
        if '本科' == degree: return 1
        if '硕士' == degree: return 2
        if '博士' == degree: return 3

    @staticmethod
    def _get_headers():
        """ 返回职位 sheet 表的标题 """
        return ['公司', '地区', '职位名称', '最低薪资', '最高薪资']

    def write_to_excel(self, excel_path, sheetname, objs):
        """ 往职位工作薄指定工作表里写数据 """
        self.xlsx_manager.switch(excel_path, sheetname)
        headers = self._get_headers()
        objs = self.list_manager.together(objs, map_=lambda x: list(x.values()))
        self.xlsx_manager.write_line(1, headers)
        self.xlsx_manager.write_lines(2, objs)

    def parse_subject_to_excel(self, dirpath):
        """ 将一个科目的数据写进 Excel """
        _, dirname = os.path.split(dirpath)
        logger.info(f'{dirname}:')
        excel_path = os.path.join(dirpath, f'{dirname}.xlsx')
        self.xlsx_manager.init(excel_path, ['本科', '硕士', '博士'], create=True)
        for filename in os.listdir(dirpath):
            degree = self._get_degree(filename)
            filepath = os.path.join(dirpath, filename)
            if not filename.endswith('.json') or not degree: continue
            objs = self.json_manager.distinct(filepath, key=lambda x: f'{x["company"]}_{x["job_name"]}')
            logger.info(f'\t{degree}: {len(objs)}')
            self.write_to_excel(excel_path, degree, objs)

    def parse(self):
        """ 将 JSON 里的数据全写进 Excel """
        if not os.path.exists(self.ROOT_PATH):
            raise FileNotFoundError
        for dirname in os.listdir(self.ROOT_PATH):
            dirpath = os.path.join(self.ROOT_PATH, dirname)
            if not os.path.isdir(dirpath): continue
            self.parse_subject_to_excel(dirpath)

    def sort_area(self):
        """ 对地区按照工作数量排序 """
        self.sorted_areas = sorted(self.areas_job_numbers.keys(),
                                   key=lambda x: self.areas_job_numbers[x], reverse=True)

    def sort_subject(self):
        """ 对专业按照工作数量排序 """
        subject_jobs_number = {}
        for item in self.analyse_data:
            subject = item['subject']
            subject_jobs_number[subject] = subject_jobs_number.get(subject, 0) + item['job_number']
        self.sorted_subjects = sorted(subject_jobs_number.keys(), key=lambda x: subject_jobs_number[x])
        self.analyse_data.sort(key=lambda x: self.sorted_subjects.index(x["subject"]), reverse=True)

    def _get_analyse_header(self):
        """ 获取分析的数据的头 """
        headers = ['搜索关键词', '搜索条件1', '搜索条件2', '招聘企业数（去重后）', '岗位数（去重后）', '平均工资']
        headers.extend(self.sorted_areas)
        return headers

    def _get_data(self, obj):
        """ 将一行数据对应的字典对象转换成列表 """
        results = [obj['subject'], '在校生/应届生', obj['degree'],
                   obj['company_number'], obj['job_number'], round(obj['avg_salary'], 2)]
        for key in self.sorted_areas:
            results.append(obj['area_map'].get(key, 0))
        return results

    def write_analyse_data(self, to_excel_path, sheetname):
        """ 将分析的结果写进汇总 Excel 文件里 """
        self.xlsx_manager.switch(to_excel_path, sheetname)
        self.sort_area(), self.sort_subject()
        self.xlsx_manager.write_line(1, self._get_analyse_header())
        results = []
        for obj in self.analyse_data:
            results.append(self._get_data(obj))
        self.xlsx_manager.append_lines(results)

    def analyse_a_sheet(self, from_excel_path, sheetname, subject):
        """ 分析某个专业下某个学位的数据 """
        self.xlsx_manager.switch(from_excel_path, sheetname)
        # 注意读取到的数据已经是按照公司、职位两个关键字去重过了
        lines = self.xlsx_manager.read(start='A2')
        companies = self.list_manager.distinct(lines, key=lambda x: x[0])
        area_map = {}  # 各地区分别有多少家企业
        job_number = len(lines)
        company_number = len(companies)
        avg_salary = 0
        for item in lines:
            # 统计不同地区有多少职业以及总薪水
            area = item[1]
            avg_salary += (float(item[3]) + float(item[4]))
            self.areas_job_numbers[area] = self.areas_job_numbers.get(area, 0) + 1
        if avg_salary > 0: avg_salary /= (len(lines) * 2)
        for item in companies:
            # 统计不同地区有多少公司
            area = item[1]
            area_map[area] = area_map.get(area, 0) + 1
        self.analyse_data.append({
            'subject': subject,
            'degree': sheetname,
            'company_number': company_number,
            'job_number': job_number,
            'avg_salary': avg_salary,
            'area_map': area_map
        })

    def analyse(self, data_dir, to_excel_path, sheetname):
        """ 基于生成的 xlsx 文件分析出各专业学位下平均工资、地区工作数等 """
        self.xlsx_manager.init(to_excel_path, [sheetname], create=True)
        for filename in os.listdir(data_dir):
            filepath = os.path.join(data_dir, filename)
            if not filename.endswith('.xlsx'): continue
            subject = filename.split('.', 1)[0]
            self.analyse_a_sheet(filepath, '本科', subject)
            self.analyse_a_sheet(filepath, '硕士', subject)
            self.analyse_a_sheet(filepath, '博士', subject)
        self.write_analyse_data(to_excel_path, sheetname)


def main():
    ana = JobAnalysis()
    # ana.parse()
    # ana.move('/Users/luyan/Desktop/职位数据')
    ana.analyse('/Users/luyan/Desktop/职位数据', '/Users/luyan/Desktop/岗位需求数据.xlsx', '汇总')


if __name__ == '__main__':
    main()
