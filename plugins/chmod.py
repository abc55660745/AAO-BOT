from nonebot import on_command, CommandSession
import nonebot
import os
import shutil
from cfg.config import read


@on_command('add_chmod', aliases=('新增权限', '新增权限'))
async def add_chmod(session: CommandSession):
    admin = read('admin', 'admin')
    if str(session.ctx['user_id']) == admin:
        accnet = session.get('accent', prompt='请输入账号')
        file = open('dict.txt', 'a+')
        file.write(accnet + ' ?\n')
        file.close()
        await session.send('添加成功')
    else:
        await session.send('您没有权限进行此操作')


def read_chmod():
    accent_list = {}
    file = open('dict.txt', 'r')
    for line in file.readlines():
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]
        accent_list[k] = v
    return(accent_list)


@on_command('chmod', aliases=('绑定账号', '绑定账号'))
async def chmod(session: CommandSession):
    accentlist = read_chmod()
    if str(session.ctx['user_id']) in accentlist:
        number = session.get('number', prompt='请输入学号')
        accentlist[str(session.ctx['user_id'])] = number
        file = open('dict.txt', 'w')
        for k, v in accentlist.items():
            file.write(str(k) + ' ' + str(v) + '\n')
        file.close()
        await session.send('学号 ' + number + ' 已成功绑定至账号 ' + str(session.ctx['user_id']))
    else:
        await session.send('您没有权限进行此操作')


@nonebot.scheduler.scheduled_job('cron', hour='0-23')
async def _():
    delList = []
    delDir = read('server', 'http_path')
    delList = os.listdir(delDir)
    for f in delList:
        filePath = os.path.join(delDir, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)
    shutil.copyfile('404.html', delDir + '404.html')


@on_command('delf', aliases=('清除文件', '删除文件'))
async def delf(session: CommandSession):
    admin = read('admin', 'admin')
    if str(session.ctx['user_id']) == admin:
        delList = []
        delDir = read('server', 'http_path')
        delList = os.listdir(delDir)
        for f in delList:
            filePath = os.path.join(delDir, f)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath, True)
        shutil.copyfile('404.html', delDir + '404.html')
        await session.send('文件已清除')
    else:
        await session.send('您没有权限进行此操作')