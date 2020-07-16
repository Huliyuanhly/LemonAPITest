import re
from scripts.handle_mysql import HandleMysql


class Parameterize:
    '''
    参数化
    '''
    not_existed_tel_pattern = r'{not_existed_tel}'  # 设置为类属性

    @classmethod
    def to_param(cls, data):
        if re.search(cls.not_existed_tel_pattern, data):
            do_mysql = HandleMysql()
            data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_existed_mobile(), data)
            do_mysql.close()
        return data


if __name__ == '__main__':
    # 注册接口参数化
    one_str = {"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "keyou"}
    print(Parameterize.to_param(one_str))
