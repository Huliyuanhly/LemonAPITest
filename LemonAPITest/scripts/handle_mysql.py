import pymysql
import random
from scripts.handle_yaml import do_yaml


class HandleMysql:
    def __init__(self):
        # 1.建立连接
        self.conn = pymysql.connect(host=do_yaml.read('mysql', 'host'),  # mysql服务器ip或者域名
                                    user=do_yaml.read('mysql', 'user'),  # 用户名
                                    password=do_yaml.read('mysql', 'password'),  # 密码
                                    db=do_yaml.read('mysql', 'db'),  # 要连接的数据库名
                                    port=do_yaml.read('mysql', 'port'),  # 数据库端口号默认为3306
                                    charset='utf8',  # 数据库编码为utf8,不能写为utf-8
                                    cursorclass=pymysql.cursors.DictCursor  # 返回的结果为字典或者嵌套字典的列表
                                    )
        # 2.使用连接对象创建游标对象
        self.cursor = self.conn.cursor()

    # def get_value(self, sql, args=None):
    #     self.cursor.execute(sql, args)
    #     self.conn.commit()
    #     return self.cursor.fetchone()
    #
    # def get_values(self, sql, args=None):
    #     self.cursor.execute(sql, args)
    #     self.conn.commit()
    #     return self.cursor.fetchall()
    @staticmethod
    def create_mobile():
        '''
        随机生成一个手机号码
        :return:
        '''
        return '188' + ''.join(random.sample('0123456789', 8))

    def is_existed_mobile(self, mobile):
        '''
        判断手机号是否被注册
        :param mobile:  指定的待查询的手机号
        :return:
        '''
        sql = do_yaml.read('mysql', 'select_user_sql')
        if self.run(sql, args=[mobile]):
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        '''
         随机生成一个数据库中没有的数据库
        :return:
        '''
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile

    def run(self, sql, args=None, is_more=False):
        self.cursor.execute(sql, args)
        self.conn.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':  # 当封装好了一个类之后，要在下面自测一下
    do_mysql = HandleMysql()
    # sql_1 = "SELECT * FROM member WHERE mobile_phone='13030780869';"
    # sql_3 = "SELECT * FROM member LIMIT 0,10;"
    # do_mysql.is_existed_mobile('18306105265')
    print(do_mysql.create_not_existed_mobile())

    # print(do_mysql.run(sql_1))
    # print(do_mysql.run(sql_3, is_more=True))
    do_mysql.close()
