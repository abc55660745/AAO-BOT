from nonebot import on_command, CommandSession
import requests
import re
import hashlib
from aip import AipOcr
import time
from icals.getClassSchedule import parseCourseTable
from icals.generateICS import create_ics, export_ics
from cfg.config import read
from datetime import datetime
from pytz import timezone
import shutil
import os
import chmod
import nonebot
from exam import get_exam_state


header = {
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'aao-eas.nuaa.edu.cn',
    'Referer': 'http://aao-eas.nuaa.edu.cn/eams/login.action',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
count = 0


def login(accent, password, session: CommandSession):
    global count, header
    APP_ID = read('baidu_API', 'APP_ID')
    APP_KEY = read('baidu_API', 'APP_KEY')
    SECRET_KEY = read('baidu_API', 'SECRET_KEY')
    client = AipOcr(APP_ID, APP_KEY, SECRET_KEY)
    r = requests.get('http://aao-eas.nuaa.edu.cn/eams/login.action', headers=header)
    session = r.cookies
    passsha = re.findall(r"CryptoJS.SHA1\('(.+?)'", r.text)[0]
    passsha = hashlib.sha1((passsha + password).encode('utf-8')).hexdigest()
    r = requests.get('http://aao-eas.nuaa.edu.cn/eams/captcha/image.action', headers=header, cookies=session)
    options = {'language_type': 'ENG'}
    if count < 499:
        yzm = client.basicAccurate(r.content, options)["words_result"]
        count = count + 1
    else:
        session.send('服务器负载过大，将使用低精度验证码识别，敬请谅解')
        yzm = client.basicGeneral(r.content, options)["words_result"]
    with open('wb.png', 'wb') as code:
        code.write(r.content)
    code.close()
    yzm = re.findall(r"words': '(.+?)'", str(yzm))[0]
    yzm = yzm.replace(' ', "")
    print(yzm)

    data = {
        'username': accent,
        'password': str(passsha),
        'captcha_response': yzm
    }
    time.sleep(1)
    r = requests.post('http://aao-eas.nuaa.edu.cn/eams/login.action', data=data, cookies=session, headers=header)
    if r.text.find('验证码不正确', 0, len(r.text)) != -1:
        return 1
    elif r.text.find('密码错误', 0, len(r.text)) != -1:
        return 0
    elif r.text.find('不存在', 0, len(r.text)) != -1:
        return 2
    else:
        return session


def get_exam(session):
    global header
    req = requests.get('http://aao-eas.nuaa.edu.cn/eams/examSearchForStd!examTable.action?allExamBatch=1',
                       headers=header, cookies=session)
    exam = req.text.replace('\t', '')
    exam = exam.replace('\n', '')
    exam = exam.replace('\r', '')
    exam = exam.replace(' ', '')
    exam = re.findall(r"<td>(.*?)</td>", exam)
    return exam


def get_week(session):
    """
    global header
    r = requests.get('http://aao-eas.nuaa.edu.cn/eams/homeExt.action', headers=header, cookies=session)
    week = re.findall(r"<font size=\"4px\">(.*?)</font>", r.text)[0]
    """
    week = ''
    return week


def get_course(session, week):
    global header
    r = requests.get('http://aao-eas.nuaa.edu.cn/eams/courseTableForStd.action', cookies=session, headers=header)
    id = r.text.replace('\n', '')
    id = id.replace(' ', '')
    id = re.findall(r'\"ids\",\"(.*?)\"\);', id)[0]
    print(id)
    data = {
        'setting.kind': 'std',
        'startWeek': week,
        'project.id': '1',
        # 'ids': '106018',
        'ids': id,
        'semester.id': '82'
    }
    r = requests.post('http://aao-eas.nuaa.edu.cn/eams/courseTableForStd!courseTable.action',
                      data=data, cookies=session, headers=header)
    return r.text


def get_grade(session):
    global header
    r = requests.get('http://aao-eas.nuaa.edu.cn/eams/teach/grade/course/person!search.action?semesterId=62',
                     cookies=session, headers=header)
    text = r.text.replace(' ', '')
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace('style=""', '')
    if text.find('<trclass="griddata-even">') != -1:
        main_grade = re.findall(r'<trclass="griddata-even">(.*?)</tr>', text)[0]
        main_grade = re.findall(r"<td>(.*?)</td>", main_grade)
        result = []
        result.append('')
        i = 0
        for project in main_grade:
            if i == 0:
                result[0] += '学年度：' + project + '\n'
            elif i == 1:
                result[0] += '学期：' + project + '\n'
            elif i == 2:
                result[0] += '门数：' + project + '\n'
            elif i == 3:
                result[0] += '总学分：' + project + '\n'
            elif i == 4:
                result[0] += '平均绩点：' + project + '\n'
            elif i == 5:
                result[0] += '必修课平均绩点：' + project + '\n'
            i += 1
        i = 0
        text = re.findall(r'<tr>(.*?)</tr>', text)
        for project in text:
            if i > 1:
                j = 0
                course = re.findall(r"<td>(.*?)</td>", text[i])
                result.append('')
                for points in course:
                    if j == 0:
                        result[i - 1] += '学年学期：' + points + '\n'
                    elif j == 2:
                        result[i - 1] += '课程序号：' + points + '\n'
                    elif j == 3:
                        result[i - 1] += '课程名称：' + points + '\n'
                    elif j == 4:
                        result[i - 1] += '课程类别：' + points + '\n'
                    elif j == 5:
                        result[i - 1] += '课程等级：' + points + '\n'
                    elif j == 6:
                        result[i - 1] += '学分：' + points + '\n'
                    elif j == 7:
                        result[i - 1] += '获得学分：' + points + '\n'
                    elif j == 8:
                        result[i - 1] += '总评成绩：' + points + '\n'
                    elif j == 9:
                        result[i - 1] += '系数：' + points + '\n'
                    elif j == 10:
                        result[i - 1] += '最终成绩：' + points + '\n'
                    elif j == 11:
                        result[i - 1] += '绩点：' + points + '\n'
                    elif j == 12:
                        result[i - 1] += '无成绩原因：' + points + '\n'
                    j += 1
            i += 1
        return result
    else:
        result = []
        result.append('没有找到成绩，如您在教务处网站上可以找到成绩请使用“反馈”指令提交bug ')
        return result


@on_command('course', aliases=('课表', '查课表'))
async def course(session: CommandSession):
    exam_state = get_exam_state(str(session.ctx['user_id']))
    if exam_state != 0:
        accentlist = chmod.read_chmod()
        http_path = read('server', 'http_path')
        address = read('server', 'address')
        if str(session.ctx['user_id']) in accentlist:
            if accentlist[str(session.ctx['user_id'])] != '?':
                accent = accentlist[str(session.ctx['user_id'])]
                password = session.get('password', prompt='请输入密 码')
                await session.send('请稍后，正在尝试连接教务系统')
                cookie = login(accent, password, session)
                if cookie == 1:
                    await session.send('验证码识别错误，请重试')
                elif cookie == 0:
                    await session.send('密码错误，请重试')
                elif cookie == 2:
                    await session.send('账号不存在，请尝试重新绑定账号')
                else:
                    time.sleep(1)
                    week = get_week(cookie)
                    table = get_course(cookie, week)
                    table = table.replace('/eams', 'http://aao-eas.nuaa.edu.cn/eams')
                    with open(http_path + str(session.ctx['user_id']) + '.html', 'w', encoding='utf-8') as f:
                        f.write(table)
                        f.close()
                    await session.send('点击网址查看课程表 http://' + address + '/' + str(session.ctx['user_id']) + '.html')
            else:
                await session.send('清先绑定账号')
        else:
            await session.send('您的账号权限不足')


@on_command('course_cal', aliases=('课表文件', '课表日历'))
async def course_cal(session: CommandSession):
    exam_state = get_exam_state(str(session.ctx['user_id']))
    if exam_state != 0:
        accentlist = chmod.read_chmod()
        http_path = read('server', 'http_path')
        address = read('server', 'address')
        if str(session.ctx['user_id']) in accentlist:
            if accentlist[str(session.ctx['user_id'])] != '?':
                accent = accentlist[str(session.ctx['user_id'])]
                password = session.get('password', prompt='请输入密 码')
                await session.send('请稍后，正在尝试连接教务系统')
                cookie = login(accent, password, session)
                if cookie == 1:
                    await session.send('验证码识别错误，请重试')
                elif cookie == 0:
                    await session.send('密码错误，请重试')
                elif cookie == 2:
                    await session.send('账号不存在，请尝试重新绑定账号')
                else:
                    time.sleep(1)
                    table = get_course(cookie, '')
                    lessons = parseCourseTable(table)
                    semester_start_date = datetime(2019, 9, 2, 0, 0, 0,
                                                   tzinfo=timezone('Asia/Shanghai'))
                    cal = create_ics(lessons, semester_start_date)
                    export_ics(cal, str(session.ctx['user_id']))
                    filename = 'NUAAiCal-Data/' + str(session.ctx['user_id']) + '.ics'
                    shutil.copyfile(os.path.abspath(filename), http_path + str(session.ctx['user_id']) + '.ics')
                    await session.send('点击网址下载日历文件 http://' + address + '/' + str(session.ctx['user_id']) + '.ics')
                    await session.send('本日历模块来自miaotony的github开源项目，感谢他对开源社区做出的贡献')
            else:
                await session.send('清先绑定账号')
        else:
            await session.send('您的账号权限不足')


@on_command('exam', aliases=('考试查询', '查考试'))
async def exam(session: CommandSession):
    exam_state = get_exam_state(str(session.ctx['user_id']))
    if exam_state != 0:
        accentlist = chmod.read_chmod()
        if accentlist[str(session.ctx['user_id'])] != '?':
            if str(session.ctx['user_id']) in accentlist:
                accent = accentlist[str(session.ctx['user_id'])]
                password = session.get('password', prompt='请输入密 码')
                await session.send('请稍后，正在尝试连接教务系统')
                cookie = login(accent, password, session)
                if cookie == 1:
                    await session.send('验证码识别错误，请重试')
                elif cookie == 0:
                    await session.send('密码错误，请重试')
                elif cookie == 2:
                    await session.send('账号不存在，请尝试重新绑定账号')
                else:
                    time.sleep(1)
                    exam = get_exam(cookie)
                    i = 0
                    flag = 0
                    text = ''
                    timet = ''
                    for project in exam:
                        if project != '':
                            if i == 0:
                                text += '课程编号：' + project + '\n'
                            elif i == 1:
                                text += '课程名称：' + project + '\n'
                            elif i == 2:
                                text += '考试类型：' + project + '\n'
                            elif i == 3:
                                text += '考试日期：' + project + '\n'
                                if project.find('未安排', 0, len(project)) == -1:
                                    timet += project + ' '
                            elif i == 4:
                                text += '考试时间：' + project + '\n'
                                if project.find('未安排', 0, len(project)) == -1:
                                    timet += project.split('~')[1] + ':00'
                            elif i == 5:
                                text += '考试地点：' + project + '\n'
                            elif i == 6:
                                text += '考试座位：' + project + '\n'
                            elif i == 7:
                                text += '考试状态：' + project + '\n'
                            i = i + 1
                        else:
                            i = 0
                            text = text.replace('<fontcolor="BBC4C3">', '')
                            text = text.replace('</font>', '')
                            if timet == '':
                                await session.send(text[:-1])
                            else:
                                timet = time.mktime(time.strptime(timet, "%Y-%m-%d %H:%M:%S"))
                                timen = time.time()
                                if timen <= timet:
                                    await session.send(text[:-1])
                                else:
                                    flag = 1
                            text = ''
                            timet = ''
                    if flag == 1:
                        await session.send('有部分过去的考试被隐藏，若需查看请使用“查询全部考试”指令查询')
            else:
                await session.send('清先绑定账号')
        else:
            await session.send('您的账号权限不足')


@on_command('examn', aliases=('全部考试', '查询全部考试'))
async def examn(session: CommandSession):
    exam_state = get_exam_state(str(session.ctx['user_id']))
    if exam_state != 0:
        accentlist = chmod.read_chmod()
        if accentlist[str(session.ctx['user_id'])] != '?':
            if str(session.ctx['user_id']) in accentlist:
                accent = accentlist[str(session.ctx['user_id'])]
                password = session.get('password', prompt='请输入密 码')
                await session.send('请稍后，正在尝试连接教务系统')
                cookie = login(accent, password, session)
                if cookie == 1:
                    await session.send('验证码识别错误，请重试')
                elif cookie == 0:
                    await session.send('密码错误，请重试')
                elif cookie == 2:
                    await session.send('账号不存在，请尝试重新绑定账号')
                else:
                    time.sleep(1)
                    exam = get_exam(cookie)
                    i = 0
                    text = ''
                    for project in exam:
                        if project != '':
                            if i == 0:
                                text += '课程编号：' + project + '\n'
                            elif i == 1:
                                text += '课程名称：' + project + '\n'
                            elif i == 2:
                                text += '考试类型：' + project + '\n'
                            elif i == 3:
                                text += '考试日期：' + project + '\n'
                            elif i == 4:
                                text += '考试时间：' + project + '\n'
                            elif i == 5:
                                text += '考试地点：' + project + '\n'
                            elif i == 6:
                                text += '考试座位：' + project + '\n'
                            elif i == 7:
                                text += '考试状态：' + project + '\n'
                            i = i + 1
                        else:
                            i = 0
                            text = text.replace('<fontcolor="BBC4C3">', '')
                            text = text.replace('</font>', '')
                            await session.send(text[:-1])
                            text = ''
            else:
                await session.send('清先绑定账号')
        else:
            await session.send('您的账号权限不足')


@on_command('grade', aliases=('成绩查询', '查成绩'))
async def grade(session: CommandSession):
    exam_state = get_exam_state(str(session.ctx['user_id']))
    if exam_state != 0:
        await session.send('此功能仍在测试状态，可能出现各种bug，如果遭遇bug请使用“反馈”指令通知管理员')
        accentlist = chmod.read_chmod()
        if accentlist[str(session.ctx['user_id'])] != '?':
            if str(session.ctx['user_id']) in accentlist:
                accent = accentlist[str(session.ctx['user_id'])]
                password = session.get('password', prompt='请输入密 码')
                await session.send('请稍后，正在尝试连接教务系统')
                cookie = login(accent, password, session)
                if cookie == 1:
                    await session.send('验证码识别错误，请重试')
                elif cookie == 0:
                    await session.send('密码错误，请重试')
                elif cookie == 2:
                    await session.send('账号不存在，请尝试重新绑定账号')
                else:
                    time.sleep(1)
                    result = get_grade(cookie)
                    for coursein in result:
                        await session.send(coursein[:-1])
            else:
                await session.send('清先绑定账号')
        else:
            await session.send('您的账号权限不足')


@nonebot.scheduler.scheduled_job('cron', hour='0')
async def _():
    global count
    count = 0
