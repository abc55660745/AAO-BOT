from nonebot import on_command, CommandSession, on_request, RequestSession
import nonebot

p1 = 0
p2 = 0
p3 = 0
p4 = 0
p5 = 0
p6 = 0


@on_command('finish', aliases=('完成', '已完成'))
async def finish(session: CommandSession):
    global p1, p2, p3, p4, p5, p6
    if session.ctx['user_id'] == 3040585972:
        topic = session.get('topic', prompt='你刚刚完成的是第几讲呢')
        await session.send('收到')
        bot = nonebot.get_bot()
        await bot.send_private_msg(user_id=3040585972, message='左清宇已完成' + topic)
    elif session.ctx['user_id'] == 2718135236:
        topic = session.get('topic', prompt='你刚刚完成的是第几讲呢')
        await session.send('收到')
        bot = nonebot.get_bot()
        await bot.send_private_msg(user_id=3040585972, message='李天豪已完成' + topic)
        p1 = 1
    elif session.ctx['user_id'] == 913637919:
        topic = session.get('topic', prompt='你刚刚完成的是第几讲呢')
        await session.send('收到')
        bot = nonebot.get_bot()
        await bot.send_private_msg(user_id=3040585972, message='陈宏昱已完成' + topic)
        p2 = 1
    elif session.ctx['user_id'] == 2039486652:
        topic = session.get('topic', prompt='你刚刚完成的是第几讲呢')
        await session.send('收到')
        bot = nonebot.get_bot()
        await bot.send_private_msg(user_id=3040585972, message='肖佳妮已完成' + topic)
        p3 = 1
    elif session.ctx['user_id'] == 2109343414:
        topic = session.get('topic', prompt='你刚刚完成的是第几讲呢')
        await session.send('收到')
        bot = nonebot.get_bot()
        await bot.send_private_msg(user_id=3040585972, message='张皓程已完成' + topic)
        p4 = 1
    elif session.ctx['user_id'] == 2582610686:
        topic = session.get('topic', prompt='你刚刚完成的是第几讲呢')
        await session.send('收到')
        bot = nonebot.get_bot()
        await bot.send_private_msg(user_id=3040585972, message='牛鑫磊已完成' + topic)
        p5 = 1
    elif session.ctx['user_id'] == 1965035986:
        topic = session.get('topic', prompt='你刚刚完成的是第几讲呢')
        await session.send('收到')
        bot = nonebot.get_bot()
        await bot.send_private_msg(user_id=3040585972, message='任钧键已完成' + topic)
        p6 = 1


@on_request('friend')
async def _(session: RequestSession):
    await session.approve()


@nonebot.scheduler.scheduled_job('cron', hour='5')
async def _():
    global p1, p2, p3, p4, p5, p6
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = 0
    p6 = 0


@nonebot.scheduler.scheduled_job('cron', hour='23')
async def _():
    bot = nonebot.get_bot()
    text = '未完成'
    global p1, p2, p3, p4, p5, p6
    if p1 != 1:
        await bot.send_private_msg(user_id=2718135236, message='今天的看完了吗')
        text = '李天豪, ' + text
    if p2 != 1:
        await bot.send_private_msg(user_id=913637919, message='今天的看完了吗')
        text = '陈宏昱, ' + text
    if p3 != 1:
        await bot.send_private_msg(user_id=2039486652, message='今天的看完了吗')
        text = '肖佳妮, ' + text
    if p4 != 1:
        await bot.send_private_msg(user_id=2109343414, message='今天的看完了吗')
        text = '张皓程, ' + text
    if p5 != 1:
        await bot.send_private_msg(user_id=2582610686, message='今天的看完了吗')
        text = '牛鑫磊, ' + text
    if p6 != 1:
        await bot.send_private_msg(user_id=1965035986, message='今天的看完了吗')
        text = '任钧键, ' + text
    if text != '未完成':
        await bot.send_private_msg(user_id=3040585972, message=text)


@nonebot.scheduler.scheduled_job('cron', hour='19,21,22')
async def _():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=947817623, message='本群提醒学习小助手提醒大家学习啦')
    await bot.send_group_msg(group_id=947817623, message='现在大家跟我一起学习郭天祥')