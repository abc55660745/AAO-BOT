#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Welcome to use the NUAA_ClassSchedule script.
模拟登录NUAA新版教务系统，获取课表，解析后生成iCal日历文件...
GitHub: https://github.com/miaotony/NUAA_ClassSchedule
Pull Requests & issues welcome!

@Author: MiaoTony, ZegWe
@Version: V0.8.1.20191113
@UpdateLog:
    V0.8.1.20191113 修复表格导出bug，完善`requirement.txt`等
    V0.8.0.20191112 新增导出课表到`.xlsx`表格文件；调换输出课程名称和教师顺序，更加符合逻辑
    V0.7.0.20191109 新增导出课表到`.txt`文件；新增匹配天目湖校区时间表；修复Issue#2 `Too Quick Click` bug；
                    删除`requirement.txt`中存在的标准库，仅保留第三方库
    V0.6.0.20191108 基于对象重构课表解析的部分功能，增加生成iCal日历文件并导出（部分参考NUAA-iCal-Python）
    V0.5.1.20191107 优化代码结构，便于下一步重构及生成iCal文件
    V0.5.0.20191107 修复因教务系统JS代码变更而无法解析课表的重大bug，增加requirement.txt
    V0.4.0.20191026 增加命令行参数解析，增加控制台输入学号密码（不回显处理），并与初始设置兼容；修复班级课表中教师为空时解析异常bug
    V0.3.1.20191018 增加解析课程所在周并优化课表输出格式，修复班级课表中班级解析bug，引入logging模块记录日志便于debug
    V0.3.0.20191017 增加 课表解析，增加 班级、实践周匹配，优化代码结构
    V0.2.1.20191012 增加UA列表，增加BeautifulSoup提取姓名学号，优化代码结构，为下一步解析课表做准备
    V0.2.0.20191010 成功登录教务系统，并成功获取个人或班级课表，但还未进行提取
    V0.1.1.20190910 加入未登录成功或过快点击的判断
    V0.1.0.20190909 尝试登录新教务系统成功，仅登录而已

"""
