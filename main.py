import nonebot
import config
from os import path
import sys


sys.path.append(sys.path[0])
sys.path.append(sys.path[0] + '/plugins')
sys.path.append(sys.path[0] + '/plugins/icals')
sys.path.append(sys.path[0] + '/plugins/cfg')
nonebot.init(config)
nonebot.load_builtin_plugins()
nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins'), 'plugins')
nonebot.run()
