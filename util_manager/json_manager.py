import os
import json


class JsonManager(object):
    """ 一个操作 JSON 的通用封装类 """

    @staticmethod
    def dump_s(obj, ensure_ascii=False, indent=2, map_=None):
        """ 将对象转换成 JSON 格式的字符串 """
        if map_ and isinstance(obj, list):
            obj = list(map(map_, obj))
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent)

    @staticmethod
    def load_s(string, filter_=None, map_=None):
        """ 将 JSON 格式字符串转换成对象返回，注意 filter_ 早于 map_ 早于 key 执行 """
        obj = json.loads(string)
        islist = isinstance(obj, list)
        if filter_ and islist:
            obj = list(filter(filter_, obj))
        if map_ and islist:
            obj = list(map(map_, obj))
        return obj

    def dump(self, obj, filepath, ensure_ascii=False, indent=2, encoding='utf-8', map_=None):
        """ 将对象转换成 JSON 格式的字符串并写进文件中 """
        dirpath, _ = os.path.split(filepath)
        os.path.exists(dirpath) or os.makedirs(dirpath)
        json_str = self.dump_s(obj, ensure_ascii=ensure_ascii, indent=indent, map_=map_)
        with open(filepath, 'w', encoding=encoding) as fp:
            fp.write(json_str)

    def load(self, filepath, encoding='utf-8', filter_=None, map_=None):
        """ 从文件读取 JSON 格式字符串并转换成对象返回 """
        if not os.path.exists(filepath):
            raise FileNotFoundError
        with open(filepath, 'r', encoding=encoding) as fp:
            return self.load_s(fp.read(), map_=map_, filter_=filter_)

    def distinct_s(self, string, filter_=None, map_=None, key=None):
        """ 传入 JSON 格式字符串，返回去重后的对象 """
        keys, results = [], []
        obj = self.load_s(string, filter_=filter_, map_=map_)
        if not isinstance(obj, list): return obj
        if not key: key = lambda x: x.__str__()
        for item in obj:
            if key(item) in keys: continue
            results.append(item)
            keys.append(key(item))
        return results

    def distinct(self, filepath, encoding='utf-8', filter_=None, map_=None, key=None):
        """ 将文件里 JSON 对象去重后返回 """
        if not os.path.exists(filepath):
            raise FileNotFoundError
        with open(filepath, 'r', encoding=encoding) as fp:
            return self.distinct_s(string=fp.read(), filter_=filter_, map_=map_, key=key)

    def classify_s(self, string, filter_=None, map_=None, key=None, diff_key=None):
        """ 从字符串里读取对象并按照某种规则分类，返回一个分类后的字典或对象本身 """
        results, diff_keys = {}, []
        obj = self.load_s(string, filter_=filter_, map_=map_)
        if not isinstance(obj, list): return obj
        if not key: key = lambda x: x.__str__()
        for item in obj:
            arr = results.get(key(item), [])
            if diff_key:
                if diff_key(item) in diff_keys: continue
                else: diff_keys.append(diff_key(item))
            arr.append(item)
            results[key(item)] = arr
        return results

    def classify(self, filepath, encoding='utf-8', filter_=None, map_=None, key=None):
        """ 从文件读取对象并分类，返回字典或对象本身 """
        if not os.path.exists(filepath):
            raise FileNotFoundError
        with open(filepath, 'r', encoding=encoding) as fp:
            return self.classify_s(string=fp.read(), filter_=filter_, map_=map_, key=key)


def main():
    manager = JsonManager()
    stus = [{'姓名': '卢研', '学校': '江苏大学'}, {'姓名': '刘妙霞', '学校': '江苏大学'}, {'姓名': '卢研', '学校': '常熟理工'}]
    stus_str = manager.dump_s(stus)
    print(manager.classify_s(stus_str, key=lambda x: x['学校'], diff_key=lambda x: x['姓名']))


if __name__ == '__main__':
    main()
