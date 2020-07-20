import re
from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import USER_ACCOUNT_FILE_PATH


class Parameterize:
    '''
    参数化
    '''
    not_existed_tel_pattern = r'{not_existed_tel}'  # 未注册的手机号
    not_existed_id_pattern = r'{not_existed_id}'  # 不存在的id

    invest_user_tel_pattern = r'{invest_user_tel}'  # 投资人的手机号
    invest_user_pwd_pattern = r'{invest_user_pwd}'  # 投资人的密码
    invest_user_id_pattern = r'invest_user_id'  # 投资人的id

    # 借款人的相关正则表达式
    borrow_user_id_pattern = r'{borrow_user_id}'  # 借款用户id
    borrow_user_tel_pattern = r'{borrow_user_tel}'  # 借款用户手机号
    borrow_user_pwd_pattern = r'{borrow_user_pwd}'  # 借款人密码

    loan_id_pattern = r'{loan_id}'
    do_user_account = HandleYaml(USER_ACCOUNT_FILE_PATH)

    @classmethod
    def to_param(cls, data):
        # 未注册手机号的参数化
        if re.search(cls.not_existed_tel_pattern, data):
            do_mysql = HandleMysql()
            data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_existed_mobile(), data)
            do_mysql.close()
        # 不存在的用户id替换
        if re.search(cls.not_existed_id_pattern, data):
            do_mysql = HandleMysql()
            sql = "SELECT id FROM member ORDER BY id DESC limit 0, 1;"
            not_existed_id = do_mysql.run(sql).get('id') + 1  # 获取最 大的id加1
            data = re.sub(cls.not_existed_id_pattern, str(not_existed_id), data)
            do_mysql.close()

        # 注册用户手机号的参数化
        if re.search(cls.invest_user_tel_pattern, data):
            invest_user_tel = cls.do_user_account.read('invest', 'mobile_phone')
            data = re.sub(cls.invest_user_tel_pattern, invest_user_tel, data)

        # 注册用户密码的参数化
        if re.search(cls.invest_user_pwd_pattern, data):
            invest_user_pwd = cls.do_user_account.read('invest', 'pwd')
            data = re.sub(cls.invest_user_tel_pattern, invest_user_pwd, data)

        # 参数化投资人的id
        if re.search(cls.invest_user_id_pattern, data):
            invest_user_id = cls.do_user_account.read('invest', 'id')
            data = re.sub(cls.invest_user_id_pattern, str(invest_user_id), data)
        # loan_id 替换
        if re.search(cls.loan_id_pattern, data):
            loan_id = getattr(cls, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)

        return data


if __name__ == '__main__':
    # 注册接口参数化
    one_str = {"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "keyou"}
    print(Parameterize.to_param(one_str))
