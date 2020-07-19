import unittest
import json
from scripts.handle_excel import HandleExcel
from libs.ddt import ddt, data
from scripts.handle_log import log
from scripts.handle_yaml import do_yaml
from scripts.handle_requests import HandleRequest
from scripts.handle_parameterize import Parameterize
from scripts.handle_mysql import HandleMysql

'''
ddt 能够实现数据驱动，通过测试用例数据，自动生成用例
自动遍历用例数据，然后去生成测试用例
每遍历出来一条测试用例，会当成一个参数传到生成的用例中去
'''


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel('recharge')
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        cls.do_request.add_headers(do_yaml.read('api', 'version'))

        cls.do_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        cls.do_mysql.close()

    @data(*cases)
    def test_case_method(self, case):  # 实例方法名不能跟模块名一致
        # 1.参数化
        new_data = Parameterize.to_param(case.data)
        # 2.拼接完整的URL
        new_url = do_yaml.read('api', 'prefix') + case.url
        # excel 中check_sql一栏不为空就去获取充值前的金额
        check_sql = case.check_sql
        if check_sql:
            check_sql = Parameterize.to_param(check_sql)
            mysql_data = self.do_mysql.run(check_sql)
            amount_before = float(mysql_data['leave_amount'])  # 是decimal类型,所以先转换成float
            amount_before = round(amount_before, 2)  # 保留为2位小数

        # 3.向服务器发起请求
        res = self.do_request.send(url=new_url,
                                   method=case.method,  # 可省略
                                   data=new_data,
                                   is_json=True  # 可省略
                                   )
        # 将响应报文中的数据转化为字典
        actual_value = res.json()

        # 获取测试用例行号
        row = case.case_id + 1
        # 获取期望值
        expected_results = case.expected  # 只做code的校验，不需要转换json
        msg = case.title  # 获取标题
        success_msg = do_yaml.read('msg', 'success_result')
        fail_msg = do_yaml.read('msg', 'fail_result')

        try:
            # assertEqual 第一个参数为期望值，第二个参数为实际值，第三个参数为用例执行失败之后的提示信息
            self.assertEqual(expected_results, actual_value.get('code'), msg=msg)
        except AssertionError as e:
            # 将响应实际值写入到actual列
            self.excel.write_data(row=row, column=do_yaml.read('excel', 'actual_col'),
                                  value=res.text)  # 响应文本是字典不能直接写入，转换文本写入

            # 将用例执行结果写入到result列
            # log.info('用例{}执行未通过'.format(case.title))
            self.excel.write_data(row=row, column=do_yaml.read('excel', 'result_col'),
                                  value=fail_msg)
            log.info(f":{msg}，执行的结果为：{fail_msg}\n,具体异常为{e}\n")
            raise e
        else:
            # log.info('用例{}执行通过'.format(case.title))
            self.excel.write_data(row=row, column=do_yaml.read('excel', 'actual_col'),
                                  value=res.text)
            self.excel.write_data(row=row, column=do_yaml.read('excel', 'result_col'),
                                  value=success_msg)
            log.info(f":{msg}，执行的结果为：{success_msg}\n")
