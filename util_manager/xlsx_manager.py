import os
import openpyxl

from openpyxl.utils.cell import get_column_letter


class XlsxManager(object):
    """ 操作 Excel 的工具类 """

    def __init__(self):
        self.wb, self.sheet = None, None
        self.filepath, self.sheetname = '', ''

    @staticmethod
    def create_excel(filepath):
        """ 返回全新的工作薄对象 """
        if not filepath.endswith('.xlsx'):
            raise ValueError('文件后缀不符')
        dirpath, _ = os.path.split(filepath)
        os.path.exists(dirpath) or os.makedirs(dirpath)
        wb = openpyxl.Workbook()
        wb.save(filepath)
        return wb

    @staticmethod
    def load_excel(filepath):
        """ 加载一个已经存在的工作薄 """
        if not filepath.endswith('.xlsx'):
            raise ValueError('文件后缀不符')
        return openpyxl.load_workbook(filepath)

    def switch(self, filepath, sheetname, create=False):
        """ 切换工作薄和工作表 """
        self.filepath, self.sheetname = filepath, sheetname
        self.wb = self.create_excel(filepath) if create else self.load_excel(filepath)
        self.sheet = self._get_sheet(sheetname=sheetname)

    def _get_sheet(self, sheetname):
        """ 从工作薄对象里获取工作表，不存在就创建 """
        if sheetname not in self.wb.sheetnames:
            self.wb.create_sheet(sheetname)
        return self.wb[sheetname]

    def _save(self):
        self.wb.save(self.filepath)

    def size(self):
        return self.sheet.max_row, self.sheet.max_column

    def read(self, slice_=None):
        """ 读取从表格数据，可以指定读取的范围 """
        results = []
        if not slice_:
            slice_ = slice('A1', f'{get_column_letter(self.sheet.max_column)}{self.sheet.max_row}')
        area = self.sheet[slice_]
        for line in area:
            tmp = []
            for cell in line:
                tmp.append(cell.value)
            results.append(tmp)
        return results

    def write(self, position, value):
        """ 往表格某个单元格里写数据 """
        self.sheet[position].value = value
        self._save()

    def write_line(self, row_number, data, need_save=True):
        """ 往表格指定行写一行数据 """
        for i, value in enumerate(data):
            self.sheet.cell(row=row_number, column=i+1).value = value
        if need_save: self._save()

    def write_lines(self, begin_row_number, datas):
        """ 往表格写很多行数据 """
        for i, data in enumerate(datas):
            self.write_line(begin_row_number + i, data, need_save=False)
        self._save()

    def append_line(self, data):
        """ 往表格追加一行数据 """
        row, _ = self.size()
        self.write_line(row + 1, data)

    def append_lines(self, datas):
        """ 往表格追加许多行数据 """
        row, _ = self.size()
        self.write_lines(row + 1, datas)


def main():
    path = '/Users/luyan/Desktop/example.xlsx'
    manager = XlsxManager()
    manager.switch(path, 'Sheet')
    print(manager.size())
    manager.append_lines([['小舞', '女', 19], ['奥斯卡', '男', 20]])


if __name__ == '__main__':
    main()
