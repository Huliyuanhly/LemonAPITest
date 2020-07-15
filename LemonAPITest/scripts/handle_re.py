import re
from scripts.handle_mysql import HandleMysql

# 1.创建待替换的字符串
one_str = {"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "keyou"}
# 正则表达式相当于一个模子，可以拿这个模子去把符合这个模子的内容全部找出来

# 2.创建正则表达式
# re_str = r'\${not_existed_tel}'
# re_str = r'{"mobile_phone":"\{not_existed_tel}'
# 正则表达式中，一定要加r，如果有些字符有特殊含义，需要在前面加\
# match方法第一个参数为正则表达式，第二个参数为待查询字符串
# match方法只能从头开始匹配
# 如果匹配不上，会返回None,如果能匹配上会返回match对象
# 可以用mtch.group()获取匹配成功后的值
# re.match(re_str, one_str)
# mtch = re.match(re_str, one_str)
# search 不用从头开始匹配，只要能匹配上，就直接返回，如果能匹配上会返回match对象，如果匹配不上会返回None
mtch = re.search(r'{not_existed_tel}', one_str)
# sub  先找到，找到之后再替换
# 第一个参数为正则表达式字符串，第二个参数为新的值，第三个参数为待替换的字符串（原始字符串）
# 如果能匹配上，会返回替换之后的值，一定为字符串类型，匹配不上会返回原始字符串
# re.sub(r'{not_existed_tel}', '18822223333', one_str)
# split
# findall
# finditer
# 在项目中 search 和sub会合在一起用
if re.search('{not_existed_tel}', one_str):
    re.sub(r'{not_existed_tel}', '18822223333', one_str)

do_mysql = HandleMysql()
real_existed_tel = do_mysql.create_not_existed_mobile()
do_mysql.close()
