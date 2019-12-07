#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
Welcome to use the NUAA_ClassSchedule script.
模拟登录NUAA新版教务系统，获取课表，解析后生成iCal日历文件...
GitHub: https://github.com/miaotony/NUAA_ClassSchedule
Pull Requests & issues welcome!

main.py  程序入口

@Author: MiaoTony, ZegWe
"""

import time
import logging
import argparse
import getpass
from datetime import datetime, timedelta
from pytz import timezone
from generateICS import create_ics, export_ics
from getClassSchedule import *
from generateXLSX import *
from settings import VERSION, DEBUG

if DEBUG:
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 设置日志级别及格式
else:
    logging.basicConfig(level=logging.WARNING,
                        format='%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 设置日志级别及格式

if __name__ == "__main__":
    # 学号及密码
    stuID = r""
    stuPwd = r""
    choice = 0  # 0 for std, 1 for class.个人课表or班级课表
    retry_cnt = 3  # 登录重试次数
    semester_year = '2019-2020'
    semester = '1'
    semester_start_date = datetime(2019, 9, 2, 0, 0, 0,
                                   tzinfo=timezone('Asia/Shanghai'))

    print("Welcome to use the NUAA_ClassSchedule script.")
    print("Author: MiaoTony\nGitHub: https://github.com/miaotony/NUAA_ClassSchedule")
    print("Version: " + VERSION + '\n')

    # Parse args 命令行参数解析
    parser = argparse.ArgumentParser()
    parser.description = 'Get NUAA class schedule at ease! 一个小jio本，让你获取课表更加便捷而实在~'
    parser.add_argument("-i", "--id", help="Student ID 学号", type=str)
    parser.add_argument("-p", "--pwd", help="Student password 教务处密码", type=str)
    parser.add_argument("-c", "--choice", help="Input `0` for personal curriculum(default), `1` for class curriculum.\
                        输入`0`获取个人课表(无此参数默认为个人课表)，输入`1`获取班级课表", type=int, choices=[0, 1])  # , default=0

    try:
        # 解析优先级高到低：命令行参数->上面的初始设置->控制台输入
        args = parser.parse_args()
        logging.info(args)

        if args.id is not None:  # 命令行参数优先
            stuID = args.id
        if args.pwd is not None:
            stuPwd = args.pwd
        if args.choice is not None:
            choice = args.choice

        if stuID == '' or stuPwd == '':  # 若学号密码为空则在控制台获取
            print('Please login!')
            stuID = input('Please input your student ID:')
            # stuPwd = input('Please input your password:')
            stuPwd = getpass.getpass('Please input your password:(不会回显，输入完成<ENTER>即可)')
            while True:
                choice = int(input('Please input your choice (`0`: personal, `1`: class):'))
                if choice in [0, 1]:
                    break
                else:
                    print('ERROR! Choice shoule be `0` or `1`!')

        temp_time = time.time()  # 计个时看看
        name = aao_login(stuID, stuPwd, retry_cnt)
        print('\nMeow~下面开始获取{}课表啦！\n'.format({0: '个人', 1: '班级'}.get(choice)))
        courseTable = getCourseTable(choice=choice)
        list_lessonObj = parseCourseTable(courseTable)
        print('课表获取完成，下面开始生成iCal日历文件啦！\n')
        cal = create_ics(list_lessonObj, semester_start_date)
        print('日历生成完成，下面开始导出啦！\n')
        #export_ics(cal, semester_year, semester, stuID)  # Export `.ics` file

    except Exception as e:
        print("ERROR! 欢迎在GitHub上提出issue & Pull Request!")
        print(e)
    finally:
        session.cookies.clear()  # 清一下cookie
