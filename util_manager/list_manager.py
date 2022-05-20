class ListManager(object):
    """ 操作 List 的工具类 """

    @staticmethod
    def together(arr, filter_=None, map_=None):
        """ 对 list 做 map 和 filter 操作，先 filter 后 map """
        if not isinstance(arr, list):
            raise TypeError
        if filter_:
            arr = list(filter(filter_, arr))
        if map_:
            arr = list(map(map_, arr))
        return arr

    @staticmethod
    def distinct(arr, key=None):
        """ 去除 arr 里面重复的元素 """
        if not isinstance(arr, list):
            raise TypeError
        keys, results = [], []
        if not key: return arr
        for item in arr:
            if key(item) in keys: continue
            results.append(item)
            keys.append(key(item))
        return results

    @staticmethod
    def classify(arr, key=None):
        """ 对 arr 里面元素进行分类 """
        if not isinstance(arr, list):
            raise TypeError
        if not key: return arr
        results = {}
        for item in arr:
            tmp = results.get(key(item), [])
            tmp.append(item)
            results[key(item)] = tmp
        return results


def main():
    data = [{'姓名': '卢研'}, {'姓名': '刘妙霞'}]
    print(ListManager.classify(data, lambda x: x['姓名']))


if __name__ == '__main__':
    main()
