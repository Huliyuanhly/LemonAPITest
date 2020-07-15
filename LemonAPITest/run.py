import unittest
import os
from datetime import datetime
from cases import test_cases
from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_log import log
from scripts.handle_yaml import do_yaml
from scripts.handle_path import REPORTS_DIR

# 创建测试套件
suite = unittest.TestSuite()
log.info('测试套件创建成功')
# 加载测试用例到测试套件
loader = unittest.TestLoader()
suite.addTest(loader.loadTestsFromModule(test_cases))
log.info('测试用例加载完毕')
# 加一个时间戳输出报告，避免后面的报告覆盖前面的报告
result_full_path = do_yaml.read('report', 'name') + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + '.html'
result_full_path = os.path.join(REPORTS_DIR, result_full_path)  # 覆盖路径
with open(result_full_path, 'wb') as fb:
    runner = HTMLTestRunner(stream=fb,
                            verbosity=2,
                            title=do_yaml.read('report', 'title'),
                            description=do_yaml.read('report', 'description'),
                            tester=do_yaml.read('report', 'tester'))
    # 执行测试套件中的测试用例
    runner.run(suite)
log.info('所有的用例已经运行完毕')
