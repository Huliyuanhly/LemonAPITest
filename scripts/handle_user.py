from scripts.handle_mysql import HandleMysql
from scripts.handle_requests import HandleRequest
from scripts.handle_yaml import do_yaml
from scripts.handle_path import USER_ACCOUNT_FILE_PATH


def create_new_user(reg_name, pwd="12345678", user_type=1):
    '''
    创建用户
    reg_name:用户昵称
    pwd:密码
    user_type:用户类型
    返回一个用户信息，嵌套字典的字典，用户昵称为key,用户信息为value
    '''
    # 建立连接 后面要关闭连接
    do_mysql = HandleMysql()
    do_request = HandleRequest()
    # 添加公共请求头
    do_request.add_headers(do_yaml.read('api', 'version'))
    url = do_yaml.read('api', 'prefix') + '/member/register'
    sql = do_yaml.read('api', 'select_user_id')  # 虽然响应报文中会返回用户ID，但是从数据库中取出，进一步数据校验了注册接口
    while True:  # 因为存在数据库中找不到手机号的可能，所以直接死循环创建一个未注册的手机号确保万无一失
        mobile_phone = do_mysql.create_not_existed_mobile()
        data = {
            "mobile_phone": mobile_phone,
            "pwd": pwd,
            "reg_name": reg_name,
            "type": user_type
        }
        # 向注册接口发起请求
        do_request.send(url, data=data)
        # 查询数据库，获取用户id
        result = do_mysql.run(sql=sql, args=(mobile_phone,))
        if result:  # 如果查询结果不为空，则获取id
            user_id = result['id']
            break
        # 构造用户信息字典
    user_dict = {
        reg_name: {
            "id": user_id,
            "mobile_phone": mobile_phone,
            "pwd": pwd,
            "reg_name": reg_name,
        }
    }

    # 关闭连接
    do_request.close()
    do_mysql.close()
    return user_dict


def generate_users_config():
    '''
    生成三个不同权限的用户
    '''
    user_datas_dict = {}
    user_datas_dict.update(create_new_user('admin', user_type=0))
    user_datas_dict.update(create_new_user('invest'))
    user_datas_dict.update(create_new_user('borrow'))
    do_yaml.write(user_datas_dict, USER_ACCOUNT_FILE_PATH)


if __name__ == '__main__':
    generate_users_config()
