import logging
import os
from scripts.handle_yaml import do_yaml
from scripts.handle_path import LOGS_DIR


class MyLogger(object):
    @classmethod
    def create_logger(cls):
        '''
        用来创建日志收集器
        :return:
        '''
        # 创建一个日志收集器

        my_log = logging.getLogger(do_yaml.read('log', 'log_name'))
        # 设置日志收集器的收集等级
        my_log.setLevel(do_yaml.read('log', 'log_level'))

        # 设置日志输出的格式
        formatter = logging.Formatter(do_yaml.read('log', 'formatter'))

        # 日志的输出
        # 创建一个输出到控制台的日志输出渠道
        sh = logging.StreamHandler()
        sh.setLevel(do_yaml.read('log', 'stream_level'))
        sh.setFormatter(formatter)

        # 将输出渠道添加到日志收集器中
        my_log.addHandler(sh)
        # 创建一个输出到文件的输出渠道
        fh = logging.FileHandler(filename=os.path.join(LOGS_DIR, do_yaml.read('log', 'logfile_name')), encoding='utf8')
        fh.setLevel(do_yaml.read('log', 'log_file_level'))
        fh.setFormatter(formatter)
        # 将输出渠道添加到日志收集器中
        my_log.addHandler(fh)
        return my_log


log = MyLogger.create_logger()  # 不要创建多个日志收集器，创建多个会重复收集

if __name__ == '__main__':
    log = MyLogger.create_logger()
    log.info('hello')
