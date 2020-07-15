import openpyxl
import os
from scripts.handle_yaml import do_yaml
from scripts.handle_path import DATAS_DIR


class CaseData:
    '''
    测试用例数据类
    '''
    pass


class HandleExcel(object):
    def __init__(self, sheetname, filename=None):
        if filename is not None:
            self.filename = os.path.join(DATAS_DIR, do_yaml.read('excel', 'cases_path'))
        else:
            self.filename = filename
        self.sheetname = sheetname

    def open(self):
        '''
        打开工作簿和表单
        :return:
        '''
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    def read_data(self):
        '''
        读取数据的方法
        :return:
        '''
        # 打开工作簿和表单
        self.open()
        # 去Excel中读取数据的代码
        rows = list(self.sh.rows)
        # 存放最终用例数据的列表
        cases = []
        # 获取表头
        title = [r.value for r in rows[0]]
        # 获取除了表头以外的数据
        for j in rows[1:]:
            data = [k.value for k in j]
            # 创建一个用例数据对象
            case = CaseData()
            # 聚合打包，然后进行遍历
            for i in zip(title, data):
                setattr(case, i[0], i[1])
            cases.append(case)
            # 关闭工作簿
        self.wb.close()
        return cases

    def write_data(self, row, column, value):
        '''
        写入数据
        :param row:
        :param column:
        :param value:
        :return:
        '''
        # 打开工作簿和表单
        self.open()
        # 写入内容
        self.sh.cell(row=row, column=column, value=value)
        # 保存文件
        self.wb.save(self.filename)
