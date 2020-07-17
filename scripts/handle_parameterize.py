import re
from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import USER_ACCOUNT_FILE_PATH


class Parameterize:
    '''
    参数化
    '''
    not_existed_tel_pattern = r'{not_existed_tel}'  # 设置为类属性
    invest_user_tel_pattern = r'{invest_user_tel}'
    invest_user_pwd_pattern = r'{invest_pwd_tel}'
    do_user_account = HandleYaml(USER_ACCOUNT_FILE_PATH)

    @classmethod
    def to_param(cls, data):
        # 未注册手机号的参数化
        if re.search(cls.not_existed_tel_pattern, data):
            do_mysql = HandleMysql()
            data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_existed_mobile(), data)
            do_mysql.close()

        # 注册用户手机号的参数化
        if re.search(cls.invest_user_tel_pattern, data):
            invest_user_tel = cls.do_user_account.read('invest', 'mobile_phone')
            data = re.sub(cls.invest_user_tel_pattern, invest_user_tel, data)

        # 注册用户密码的参数化
        if re.search(cls.invest_user_pwd_pattern, data):
            invest_user_pwd = cls.do_user_account.read('invest', 'pwd')
            data = re.sub(cls.invest_user_tel_pattern, invest_user_pwd, data)

        return data


if __name__ == '__main__':
    # 注册接口参数化
    one_str = {"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "keyou"}
    print(Parameterize.to_param(one_str))
