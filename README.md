AAO-BOT
=======
[点此访问本项目GitHub仓库](https://github.com/abc55660745/AAO-BOT)  

概述
___
最近教务处进行了一波坑爹更新，御道南航也不能使了  
就花了两个周末写了这个教务处机器人  
通过百度的文字识别API识别验证码进行登陆（教务处这个验证码也太垃圾了  
本机器人基于coolq的HTTP-API运行  
使用了[NUAA_ClassSchedule](https://miaotony.github.io/NUAA_ClassSchedule/)
和[nonebot](https://github.com/richardchien/nonebot)两个开源项目  
如果懒得搭建运行环境的话也可以把plugins/aao_eas里相关的函数直接导入到你的项目里  
（记得把所有使用了read函数获得的常量值使用你的值替代  
如果在使用过程中出现了无法解决的bug，请提issue，我有时间会来解决

声明
___
本机器人所有信息均从[教务处网站](http://aao-eas.nuaa.edu.cn)上爬取，
本人不对数据真实性做任何保障，请自行核对数据是否正确  
禁止将本机器人运用于违法行为，本人不对其他人使用本程序导致的任何后果负责  
禁止本机器人用于商用，这是为了大家方便才开发的东西  
由于个人隐私考虑没有将密码存储于服务器上，可以自行开发相关功能

部署
____
使用本机器人需要先搭建coolq服务器并安装需要的插件
（可参考[这篇文档](https://cqhttp.cc/docs/4.12/#/)进行设置  
机器人需要python3.6以上的版本，并执行以下命令安装所必须的模块
```shell script
pip install nonebot
pip install baidu-aip
pip install APScheduler
pip install requests
pip install bs4
pip install openpyxl
pip install icalendar

yum install libxslt-devel
yum install libxml2-devel
pip install lxml
```
注意：安装lxml时需要两个前置包，以上是在CentOS下所需要的安装指令，请自行转换  
除上述以外，机器人的课表相关指令的返回依靠http服务，需要自行部署http服务器
全部就绪以后执行main.py就好啦

配置
____
目前版本有config.ini与config.py两个文件存储所需的配置，其中config.py的配置可参考
[nonebot官方文档](https://nonebot.cqp.moe/guide/basic-configuration.html)  
config.ini下则是机器人所需要的配置文件，下面一项一项介绍
- baidu-API  
    该分类下所有配置均是百度文字识别的调用API，请参考你在百度智能云的应用管理界面的信息填写  
    就算没有也可去创建一个，每天免费调用500次也基本够用，具体方法请自行搜索
- admin  
    这个分类下暂时只有admin一个项目，该项目需要指向一个QQ号  
    用于用户调用“反馈”时进行反馈，以及“新增权限”和“群发”指令的权限鉴定
- server  
    该分类主要用于存储服务器地址相关的信息
    - address  
        该项目需要指向一个远程地址，机器人返回课表以及日历文件使用的是http连接的方式，
        这里应指向http服务器的远程地址  
    - http_path  
        该项目需要指向一个本地地址，该地址应为http服务器根目录，用于写入需要返回的信息

使用
____
现在使用支持以下指令  
```
//教务处相关  该部分所有指令的学号将从dict.txt中读取，密码将再次询问

课表/查课表           //用于查询课表，返回一个网页，打开即可查看
课表文件/课表日历     //用于生成日历文件，可将其导入到手机日历中！注意！目前已知华为手机无法导入
考试查询/查考试       //用于查询考试信息，将按场次返回考试信息！注意！已经过去的考试将不会显示（以服务器时间为准
全部考试/查询全部考试 //用于查询考试信息，将返回包括已过去的考试在内的所有考试信息
成绩查询/查成绩       //用于查询成绩，将返回学期整体情况和每科的成绩！！！注意！！！该功能正在开发，存在大量bug

//权限管理相关

新增权限             //该指令仅能由管理员使用，将再次询问需要新增权限的对象，需回复一个QQ号
绑定账号             //该指令任何人都可以使用，用于绑定自己的学号
清除文件/删除文件     //该指令仅能由管理员使用，将立即清除服务器上产生的所有个人信息（指http服务器根目录

//其他

群发   //应该不用我再解释了，仅能由管理员使用，用于群发公告
反馈   //任何人可用，应该也不用我解释了
```

Version
_______
>1.0.1 修复了群发功能无法正常返回发送成功的问题  

>1.0.0 本机器人经过半个月的内部测试后正式发布1.0版，除查成绩以外其他功能趋于稳定

Bugs
____
- 目前已知查成绩功能功能存在大量bug
  - 当存在多个学期时无法正常区分
  - 当存在多门课程时出现排版错误
  - 部分账号可能出现没有回应的现象
 - 验证码识别率依然不太理想，接下来将新增验证码回显的功能
 - 目前仅使用了大一的账号进行测试，其他年级包括进入下学期后可能无法正常连接教务处
