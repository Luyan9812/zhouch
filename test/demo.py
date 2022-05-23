import re
import os

from util_manager.json_manager import JsonManager
from util_manager.xlsx_manager import XlsxManager


json_manager = JsonManager()
xlsx_manager = XlsxManager()
_root_path = '/Users/luyan/Downloads/zhouch/jobs'


def data_headers():
    return ['公司', '地区', '职位名称', '最低薪资', '最高薪资']


def progress_headers():
    return ['专业', '学位', '已获取数据数', '已获取数据页数', '是否爬取结束']


def write_json_to_excel(json_path, excel_path):
    _, json_name = os.path.split(json_path)
    pattern = '(.*?)\[(.*?), (.*?), (True|False)].json'
    result = re.match(pattern, json_name)
    subject, degree, numbers, finished = result.group(1), result.group(2), int(result.group(3)), result.group(4)
    print(subject, degree)
    data = json_manager.load(json_path, map_=lambda x: x.values())
    xlsx_manager.switch(excel_path, degree)
    xlsx_manager.write_line(1, data_headers())
    xlsx_manager.append_lines(data)
    xlsx_manager.switch(excel_path, 'progress')
    if xlsx_manager.size() == (0, 0):
        xlsx_manager.write_line(1, progress_headers())
    numbers = 0 if numbers < 0 else numbers
    pages = numbers // 50 + (1 if numbers % 50 != 0 else 0)
    xlsx_manager.append_line([subject, degree, numbers, pages, finished])


def main():
    for dirname in os.listdir(_root_path):
        dirpath = os.path.join(_root_path, dirname)
        if not os.path.isdir(dirpath): continue
        excel_path = os.path.join(dirpath, f'_{dirname}.xlsx')
        xlsx_manager.init(excel_path, ['本科', '硕士', '博士', 'progress'], create=True)
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if not filename.endswith('.json'): continue
            write_json_to_excel(filepath, excel_path)


if __name__ == '__main__':
    main()
    # print(type(eval('True')), eval('False'))
