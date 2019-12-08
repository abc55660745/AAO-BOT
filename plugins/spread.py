from nonebot import on_command, CommandSession
import nonebot
from cfg.config import read


@on_command('spread', aliases=('群发', '发送公告'))
async def spread(session: CommandSession):
    admin = read('admin', 'admin')
    if str(session.ctx['user_id']) == admin:
        text = session.get('text', prompt='请输入内容')
        file = open('dict.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            k = int(line.split(' ')[0])
            bot = nonebot.get_bot()
            if k != '11111':
                await bot.send_private_msg(user_id=k, message=text)
        await session.send('发送成功')
    else:
        await session.send('您没有权限进行此操作')
