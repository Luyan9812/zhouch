import re
import os


class FileManager(object):
    """ 封装常见文件操作 """

    @staticmethod
    def list_sub_dirs(path, pattern='.*', need_fullpath=False):
        """ 获取某个目录下所有的子目录名称，若 need_fullpath=True 则返回子目录完整路径列表 """
        results = []
        if not os.path.isdir(path):
            raise ValueError(f'路径 "{path}" 不存在或不是目录')
        for dirname in os.listdir(path):
            dirpath = os.path.join(path, dirname)
            if os.path.isdir(dirpath) and re.fullmatch(pattern, dirname): results.append(dirname)
        if not need_fullpath: return results
        return list(map(lambda x: f'{os.path.join(path, x)}', results))

    @staticmethod
    def list_sub_files(path, pattern='.*', need_fullpath=False):
        """ 获取某个目录下所有的子文件名称，若 need_fullpath=True 则返回子文件完整路径列表 """
        results = []
        if not os.path.isdir(path):
            raise ValueError(f'路径 "{path}" 不存在或不是目录')
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath) and re.fullmatch(pattern, filename):
                results.append(filename)
        if not need_fullpath: return results
        return list(map(lambda x: f'{os.path.join(path, x)}', results))


def main():
    print(FileManager.list_sub_files('/Users/luyan/Downloads/zhouch/jobs'))


if __name__ == '__main__':
    main()
