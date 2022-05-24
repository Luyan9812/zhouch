from functools import reduce


class ListManager(object):
    """ 操作 List 的工具类 """

    @staticmethod
    def together(arr, filter_=None, map_=None, reduce_=None):
        """ 对 list 做 map 和 filter 操作，先 filter 后 map """
        if not isinstance(arr, list):
            raise TypeError
        if filter_:
            arr = list(filter(filter_, arr))
        if map_:
            arr = list(map(map_, arr))
        if reduce_:
            arr = reduce(reduce_, arr)
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

    @staticmethod
    def find(arr, ele, key=None):
        if not key: key = lambda x: x
        for i, item in enumerate(arr):
            if key(ele) == key(item): return i
        return -1


def main():
    data = [{'姓名': '小明'}, {'姓名': '小华'}]
    print(reduce(lambda x1, x2: x1['姓名'] + x2['姓名'], data))


if __name__ == '__main__':
    main()
