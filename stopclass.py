from tkinter import *
from datetime import datetime
from tkinter.messagebox import *
import sys
import json
import os
import threading#多线程库
from multiprocessing import  Process#多进程库
import time
import ctypes#退出线程用的底层库
import inspect#同上
import logging
import traceback
import getopt
from urllib import request
import json
def fetch_data(url):
    '''该函数部分借鉴了https://blog.csdn.net/qq_41800366/article/details/85847218'''
    req = request.Request(url,headers=headers)
    with request.urlopen(req) as f:     # 打开url请求（如同打开本地文件一样）
        return json.loads(f.read().decode('utf-8'))  # 读数据 并编码同时利用json.loads将json格式数据转换为python对象

version='V1.5.2'
headers={'Accept':'application/json','User-Agent':'StopClass Client '+version}
class TestTime(object):
    def __init__(self, master=None):
        self.root = master
        self.updatetime()
    def tryclose(self):
        logging.debug('尝试关屏')
        self.w_com=Toplevel()
        self.w_com.title('Result')
        self.text_com=Text(self.w_com)
        self.text_com.pack(side=TOP, fill=BOTH)
        self.text_com.insert(END,os.popen('closedisplay').readline())
    def debug(self,event):
        logging.info('Open Debug Mode')
        self.root.wm_attributes('-topmost',0)#取消主窗口置顶
        self.w_debug=Toplevel()
        self.w_debug.title('Debug Mode')
        self.w_debug.wm_attributes('-topmost',1)#分窗口置顶
        self.buttonA=Button(self.w_debug,text='Close Display',command=self.tryclose)
        self.buttonA.pack()
        self.buttonB=Button(self.w_debug,text='Close App',command=force_exit)
        self.buttonB.pack()
        self.buttonC=Button(self.w_debug,text='Shutdown System',command=lambda:os.system('shutdown -s'))
        self.buttonC.pack()
        self.buttonD=Button(self.w_debug,text='Reboot System',command=lambda:os.system('shutdown -r'))
        self.buttonD.pack()
        self.buttonE=Button(self.w_debug,text='Check Log',command=self.check_log)
        if not enable_log:
            self.buttonE.configure(state='disabled')
        self.buttonE.pack()
        self.LabelAb=Label(self.w_debug,text='Copyright © 2021-2022 License:AGPL  WJZ\nPowered by Tkinter on Python\nVersion:'+version+'\nGithub Repo:\nhttps://github.com/123ABCDF11345/fuck_school')
        self.LabelAb.pack()
    def check_log(self):
        logging.debug('读日志')
        self.w_com=Toplevel()
        self.w_com.title('Log')
        self.text_com=Text(self.w_com)
        self.text_com.pack(side=TOP, fill=BOTH)
        with open('./fucker.log','r') as fp:
            self.text_com.insert(END,fp.read())
    def updatetime(self):
        self.labelE = Label(self.root, text='\n  距离'+time_title+'还有：',font = ('黑体' , 75))#这里的title也是全局变量
        self.labelE.bind_all('<F10>', self.debug)
        self.labelE.pack()
        self.labelF = Label(self.root, text="",font = ('黑体' , 75),fg='red')#空label等待更新
        self.labelF.pack()
        self.labelT = Label(self.root, text="",font = ('黑体' , 25))#空label等待更新
        self.labelT.pack()
        self.labelG = Label(self.root,text=history,font = ('黑体' , font_number))
        self.labelG.pack()
        self.labelH = Label(self.root,text=full_message,font = ('黑体' , 18))
        self.labelH.pack()
        self.updateC()

    def updateC(self):
        # 获取当日日期，不包含时间，str
        self.nowday = datetime.now().strftime("%Y-%m-%d")
        # 字符串拼接，组成当日expect time
        a = self.nowday + ' '+final_time#注意这里的finaltime是全局变量
        self.newtime = datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
        t=list(str(self.newtime - datetime.now()).split('.')[0])#得出来的时间精确到毫秒，用split干掉毫秒之后的内容
        if ',' in t:#超过一天的处理
            t=t[t.index(',')+2:]#删去天数，保留小时 注意+2是因为>1天时有['-', '1', ' ', 'd', 'a', 'y', ',', ' ',时间],这里删掉空格
        if t[0]=='0' and t[1]==':':#处理掉0的小时占位，这里之所以不用replace要考虑0:10:00会变成100，必须要求第一位是0，防止10:00:00这种
            t=t[2:]
        self.labelF.configure(text=t)
        # print(t)
        if t == ['0', '0', ':', '0', '0']:
            force_exit()
        self.root.after(1000, self.updateC)#1000ms更新倒计时


def showit():
    str_message='''
 现在课程多，害死人，使中小学生、大学生天天处于紧张状态。

 课程可以砍掉一半。学生成天看书，并不好，可以参加一些生产劳动和必要的
社会活动。

 现在的考试，用对付敌人的办法，搞突然袭击，出一些怪题、偏题，整学生。\
这是一种考八股文的方法，我不赞成，要完全改变。我主张题目公开，由学生研究、\
看书去做。例如，出二十个题，学生能答出十题，答得好，其中有的答得很好，有\
创见，可以打一百分；二十题都答了，也对，但是平平淡淡，没有创见的，给五十\
分、六十分。考试可以交头接耳，无非自己不懂，问了别人懂了。懂了就有收获，\
为什么要死记硬背呢？人家做了，我抄一遍也好。可以试试点。
                                                       ---伟大的革命导师毛主席
'''
    showwarning('Fuck School',str_message)

def timetoclose(window):
    logging.debug('window close:'+str(type(window)))
    try:
        window.destroy()#销毁窗口
    except RuntimeError:
        pass
def force_exit():
    timetoclose(root)
    if enable_taskmgr:
        killer.terminate()#停止子进程
    sys.exit()

class Taskmgr_Killer(Process): #继承Process类
    '''多进程类实现
    在这个类里面print在windows环境下用不了
    logging模块不支持多进程，所以暂时没办法打日志'''
    def __init__(self):
        super(Taskmgr_Killer,self).__init__()#父类初始化
        self.name = 'taskmgr_killer'#重写进程名
        '''没法打的日志
        self.logger=logging.getLogger('logger')
        self.h1 = logging.FileHandler('killer.log')
        self.h1.setLevel(logging.DEBUG)
        self.h1.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s]  :  %(message)s'))
        self.logger.addHandler(self.h1)'''
        logging.info('子进程激活')
    def isRunning(self,process_name):
        '''判断某一进程是否在运行'''
        try:
            #print('tasklist | findstr '+process_name)
            process=len(os.popen('tasklist | findstr /I '+process_name).readlines())#不区分大小写
            #print(process)
            if process >=1 :
                with open('killer.log','w') as fp:
                    fp.write('检测到任务管理器运行')
                #self.logger.info('检测到任务管理器运行')
                return True
            else:
                return False
        except Exception as e:
            with open('killer.log','w') as fp:
                fp.write(e,traceback.format_exc())

            #self.logger.error("Taskmgr_Killer error:")
            #self.logger.error(e)
            #self.logger.error(traceback.format_exc())
            return False

    def run(self):
        '''干掉任务管理器'''
        while 1:
            if self.isRunning('taskmgr.exe'):
                os.system('taskkill /IM taskmgr.exe')
                #self.logger.info('关闭任务管理器')
            time.sleep(1)

def check_arg(argv):
    global lite_mode,final_time,time_title,full_screen,enable_taskmgr,enable_log,zoomed,window_name
    try:
        opts, args = getopt.getopt(argv, "hlz", ["time=","window-name=", "enable-log=","enable-taskmgr_killer",'lite','title=','without-full-screen'])
    except getopt.GetoptError:#传参错误拦截
        showwarning('',"无效参数，输入-h 获取帮助信息")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-h']:
            showinfo('','''Help Message For Fuck School '''+version+'''\ndeveloper:123ABCDF11345 汪俊择 License:AGPL-3.0
-----------
参数
-h : 显示帮助
-l,--lite : 简洁模式
--time (str)(%H:%M:%S) ： 指定倒计时时间，格式为%H:%M:%S
--enable-taskmgr_killer : 检测任务管理器进程
--enable-log (str): 启用日志，日志级别为(str):支持DEBUG INFO WARNING ERROR
--title (str) : 指定显示标题
--without-full-screen : 不使用全屏
-z,--zoomed : 窗口最大化
--window-name : 指定窗口名
-----------
默认表现：
  完整模式
  禁用日志
  关闭检测任务管理器进程
  全屏显示
-----------
注意
  当使用-z或--zoomed参数时会自动启用--without-full-screen
  当使用--without-full-screen参数时不会激活zoomed状态
  当使用-l参数时不会激活--without-full-screen参数
  当不使用-z或-zoomed或--without-full-screen参数时window-name参数会执行，但屏幕不会出现''')
            sys.exit()
        elif opt in ['-l','--lite']:
            lite_mode=True
        elif opt in ['--time']:
            try:
                datetime.strptime(arg, '%H:%M:%S')
            except ValueError:
                showwarning('','time传参错误，期望的参数是%H:%M:%S')
                sys.exit(2)
            else:
                final_time=arg#留参备用
        elif opt in ['--enable-log']:
            enable_log=True
            if arg in ['DEBUG','INFO','WARNING','ERROR']:
                logging.basicConfig(filename='fucker.log',filemode='w',level=arg, format='[%(asctime)s] [%(levelname)s]  :  %(message)s',datefmt='%Y-%m-%d %I:%M:%S')
            else:
                showwarning('',"enable-log传参错误，期望的参数是['DEBUG','INFO','WARNING','ERROR']")
                sys.exit(2)
        elif opt in ['--enable-taskmgr_killer']:
            enable_taskmgr=True
        elif opt in ['--title']:
            time_title=arg
        elif opt in ['--without-full-screen']:
            full_screen=False
        elif opt in ['--zoomed','-z']:
            zoomed='zoomed'
            full_screen=False
        elif opt in ['--window-name']:
            window_name=arg
if __name__ == '__main__':
    '''命令行参数检测'''
    time_title='unknown'
    final_time='23:59:59'
    enable_taskmgr=False
    lite_mode=False
    enable_log=False
    zoomed='normal'
    window_name='Fuck School'
    full_screen=True#初始的变量值
    root = Tk()#提前创建窗口
    check_arg(sys.argv[1:])
    logging.info('主进程激活')
    font_number=18#定义信息字体大小
    history=''#如果是lite_mode就会留空
    full_message=''#同上
    #print(str_date)
    if lite_mode==False:#获取历史上的今天
        if len(str(datetime.now().month))==1:
            month='0'+str(datetime.now().month)
        else:
            month=str(datetime.now().month)
        if len(str(datetime.now().day))==1:
            day='0'+str(datetime.now().day)
        else:
            day=str(datetime.now().day)
        str_date=month+day
        try:
            admin_message=fetch_data('https://class.api.askdream.top:88/v2/list')
            try:
                admin_message=admin_message[str_date]
            except KeyError:
                try:
                    data=fetch_data('https://www.ipip5.com/today/api.php?type=json')['result']
                    logging.debug(str(data))
                except Exception as e:
                    history=''
                    logging.error("Main program error when get today data:")
                    logging.error(e)
                    logging.error(traceback.format_exc())
                else:
                    for i in range(0,15,2):
                        use_data=data[i]
                        today_message=use_data['year'].replace('\n',"")+'年，'+use_data['title']
                        if '2022年' in today_message:
                            today_message=''
                            logging.debug('已移除API内容')
                        if 'www.ipip5.com' in today_message:
                            today_message=''
                        full_message=full_message+'\n'+today_message
                    history='\n\n\n\n历史上的今天'
            else:
                logging.info('获取到公告数据，覆写历史上的今天')
                history='\n\n'+admin_message
                font_number=21
        except Exception as e:
            history=''
            logging.error('API连接失败！')
            logging.error("Main program error when get API data:")
            logging.error(e)
            logging.error(traceback.format_exc())
    if enable_taskmgr:#启用任务管理器子进程
        killer=Taskmgr_Killer()
        killer.start()
    root.state(zoomed)
    root.title(window_name)
    root.attributes('-fullscreen', full_screen)#交给命令行检测函数处理后的变量full_screen
    if not lite_mode:
        '''这些是强制技术'''
        #5秒提示
        message2=Label(root,text='\n无 声 的 抗 议',font = ('黑体' , 19))
        message2.pack()
        threading.Timer(5, timetoclose, args=(message2,)).start()#定时器线程，5s后关闭提示
        #上面一行message2后面的逗号不能删，删了要报TypeError,不知道为什么
        root.wm_attributes('-topmost',1)
        #拦截窗口关闭事件
        root.protocol("WM_DELETE_WINDOW",showit)
    #倒计时类实例
    TestTime(root)
    #窗口锁定置顶
    root.mainloop()
