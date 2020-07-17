import os

one_path = os.path.abspath(__file__)
print(one_path)
two_path = os.path.dirname(one_path)
three_path = os.path.dirname(two_path)
# 项目根目录路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# 获取配置文件所在的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')
# 例外操作
# 获取配置文件所在的路径
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, 'testcase01.yaml')
# 获取日志文件所在的目录路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
# 获取报告文件所在的目录路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
# 获取Excel所在的目录路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')
# 获取用户信息配置的路径
USER_ACCOUNT_FILE_PATH = os.path.join(CONFIGS_DIR, 'user_account.yaml')
# 测试用例模块所在目录路径
CASES_DIR = os.path.join(BASE_DIR, 'cases')
pass
