from nonebot import on_command, CommandSession
import nonebot
from cfg.config import read


@on_command('report', aliases=('反馈', '反馈问题'))
async def report(session: CommandSession):
    text = session.get('text', prompt='请输入要反馈的内容')
    bot = nonebot.get_bot()
    admin = read('admin', 'admin')
    await bot.send_private_msg(user_id=admin, message=str(session.ctx['user_id']) + '反馈问题：\n' + text)
    await session.send('反馈成功')
