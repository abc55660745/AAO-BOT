import configparser

conf = configparser.ConfigParser()


def read(section, name):
    conf.read('config.ini')  # 文件路径
    info = conf.get(section, name)  # 获取指定section 的option值
    return info
