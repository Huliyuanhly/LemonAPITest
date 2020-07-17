import unittest
import json
from scripts.handle_excel import HandleExcel
from libs.ddt import ddt, data
from scripts.handle_log import log
from scripts.handle_yaml import do_yaml
from scripts.handle_requests import HandleRequest
from scripts.handle_parameterize import Parameterize

'''
ddt 能够实现数据驱动，通过测试用例数据，自动生成用例
自动遍历用例数据，然后去生成测试用例
每遍历出来一条测试用例，会当成一个参数传到生成的用例中去
'''


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel('login')
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        cls.do_request.add_headers(do_yaml.read('api', 'version'))

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()

    @data(*cases)
    def test_case_method(self, case):  # 实例方法名不能跟模块名一致
        # 1.参数化
        new_data = Parameterize.to_param(case.data)
        # 2.拼接完整的URL
        new_url = do_yaml.read('api', 'prefix') + case.url
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
        expected_results = json.loads(case.expected, encoding="utf-8")
        msg = case.title  # 获取标题
        success_msg = do_yaml.read('msg', 'success_result')
        fail_msg = do_yaml.read('msg', 'fail_result')

        try:
            # assertEqual 第一个参数为期望值，第二个参数为实际值，第三个参数为用例执行失败之后的提示信息
            self.assertEqual(expected_results, actual_value.get('code'), msg=msg)
            self.assertEqual(expected_results.get('msg'), actual_value.get('msg'), msg=msg)
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
