import os

from util_manager.json_manager import JsonManager
from util_manager.xlsx_manager import XlsxManager


class Job51Helper(object):
    """ 操作 Job51 配置文件的类 """

    _data_dir = '/Users/luyan/Downloads/zhouch/jobs'
    _degrees_map = {'本科': 1, '硕士': 2, '博士': 3}
    _subjects = ['计算机', '经济学', '财政学', '金融', '经济与贸易', '法学', '政治', '社会学', '马克思主义', '教育学', '汉语言文学',
                 '汉语国际教育', '英语', '俄语', '德语', '法语', '西班牙语', '阿拉伯语', '日语', '韩语', '葡萄牙语', '意大利语',
                 '新闻', '广告', '网络与新媒体', '历史', '数学', '物理', '地理', '大气', '生物科学', '生物工程', '心理', '统计',
                 '力学', '机械', '工业设计', '车辆工程', '仪器', '材料', '新能源', '能源动力', '电气', '电子信息', '电子科学',
                 '通信工程', '微电子', '光电信息', '人工智能', '自动化', '土木', '水利', '测绘', '化工', '制药工程', '地质', '矿业',
                 '轻工', '交通运输', '交通工程', '海洋工程', '航空航天', '兵器', '农业工程', '林业工程', '环境科学', '生物医学工程',
                 '食品科学与工程', '建筑学', '城乡规划', '风景园林', '安全工程', '动物医学', '动物科学', '水产', '药学', '中药学',
                 '工程管理', '工程造价', '工程审计', '会计学', '财务管理', '国际商务', '人力资源管理', '审计学', '资产评估',
                 '物流管理', '物流工程', '供应链管理', '工业工程', '电子商务', '知识产权', '运动康复', '化学', '给排水', '港口',
                 '勘查', '服装设计', '交通运输', '轨道交通', '飞行器', '环境', '医学检验技术', '医学影像技术', '口腔医学技术',
                 '康复治疗', '医学影像学']

    def __init__(self, settings_path):
        self._progress_list = []
        self.xlsx_manager = XlsxManager()
        self.json_manager = JsonManager()
        self.settings_path = settings_path

    @property
    def progress_list(self):
        """ 爬取进度所在的列表 """
        if not self._progress_list:
            self.read()
        return self._progress_list

    def read(self):
        """ 读取爬取记录，有配置文件就从配置文件读取，否则从存储目录解析 """
        self.load_from_settings_file() if os.path.exists(self.settings_path) else self.scan()
        for item in self._progress_list:
            if isinstance(item[4], str):
                item[4] = eval(item[4])
            else: print(item, type(item[4]))

    def scan(self):
        """ 扫描本地目录获取已爬取记录 """
        for dirname in os.listdir(self._data_dir):
            dirpath = os.path.join(self._data_dir, dirname)
            if not os.path.isdir(dirpath): continue
            for filename in os.listdir(dirpath):
                filepath = os.path.join(dirpath, filename)
                if not filename.startswith('_'): continue
                self.xlsx_manager.switch(filepath, 'progress')
                self._progress_list.extend(self.xlsx_manager.read(start='A2'))
        subject_degree_list = list(map(lambda x: [x[0], x[1]], self._progress_list))
        for subject in self._subjects:
            for degree in self._degrees_map:
                if [subject, degree] in subject_degree_list: continue
                self._progress_list.append([subject, degree, 0, 0, 'False'])
        self._progress_list.sort(key=lambda x: (x[0], self._degrees_map[x[1]]))
        self.write_to_settings_file()

    def load_from_settings_file(self):
        """ 从配置文件加载爬取进度 """
        self._progress_list = self.json_manager.load(self.settings_path)

    def write_to_settings_file(self):
        """ 将读取的进度写进配置文件 """
        with open(self.settings_path, 'w', encoding='utf-8') as fp:
            fp.write('[')
            last_subject = ''
            for i, item in enumerate(self._progress_list):
                if last_subject != item[0]:
                    fp.write('\n\t')
                    last_subject = item[0]
                fp.write(f'["{item[0]}", "{item[1]}", {item[2]}, {item[3]}, "{item[4]}"]')
                if i < len(self._progress_list) - 1: fp.write(', ')
            fp.write('\n]')


def main():
    helper = Job51Helper('/Users/luyan/Documents/PyCharm/zhouch/generator/settings/Job51UrlGenerator.gs')
    print(helper.progress_list)


if __name__ == '__main__':
    main()
    # print(["name"] in [['name'], ['age']])
