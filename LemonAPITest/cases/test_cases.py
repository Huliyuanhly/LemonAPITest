import unittest
import os
from scripts.handle_excel import HandleExcel
from cases.register import register
from libs.ddt import ddt, data
from scripts.handle_log import log
from scripts.handle_yaml import do_yaml
from scripts.handle_path import DATAS_DIR

'''
ddt 能够实现数据驱动，通过测试用例数据，自动生成用例
自动遍历用例数据，然后去生成测试用例
每遍历出来一条测试用例，会当成一个参数传到生成的用例中去
'''


@ddt
class TestCaseRegister(unittest.TestCase):
    excel = HandleExcel('register')
    cases = excel.read_data()

    @data(*cases)
    def test_case_method(self, case):
        # 获取测试用例行号
        row = case.case_id + 1
        # 第一步 准备测试用例数据
        expected = eval(case.expected)
        data1 = eval(case.data)
        # 第二步 调用功能函数 获取实际结果
        res = register(*data1)
        # 第三步 比对预期结果和实际结果
        try:
            self.assertEqual(res, expected)
        except AssertionError as e:
            log.info('用例{}执行未通过'.format(case.title))
            self.excel.write_data(row=row, column=do_yaml.read('excel', 'result_col'),
                                  value=do_yaml.read('msg', 'fail_result'))
            log.error(f"断言异常:{e}")
            raise e
        else:
            log.info('用例{}执行通过'.format(case.title))
            self.excel.write_data(row=row, column=do_yaml.read('excel', 'result_col'),
                                  value=do_yaml.read('msg', 'success_result'))
