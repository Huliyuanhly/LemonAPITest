import yaml
from configparser import ConfigParser
from scripts.handle_path import CONFIG_FILE_PATH


class HandleYaml:
    def __init__(self, filename):
        with open(filename, encoding='utf-8') as one_file:
            self.datas = yaml.full_load(one_file)

    def read(self, section, option):
        return self.datas[section][option]

    @staticmethod
    def write(datas, filename):
        with open(filename, 'w', encoding='utf-8') as one_file:
            yaml.dump(datas, one_file, allow_unidoce=True)


do_yaml = HandleYaml(CONFIG_FILE_PATH)
if __name__ == '__main__':
    do_yaml = HandleYaml(CONFIG_FILE_PATH)
    pass
