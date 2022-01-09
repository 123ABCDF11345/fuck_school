from tkinter import *
from datetime import datetime
from tkinter.messagebox import *
import sys
import json
import requests
import os
import threading
headers={'Accept':'application/json','User-Agent':'StopClass Client 2.0'}
class TestTime(object):
    def __init__(self, master=None):
        self.root = master
        self.updatetime()
    def tryclose(self):
        self.w_com=Toplevel()
        self.w_com.title('Result')
        self.text_com=Text(self.w_com)
        self.text_com.pack(side=TOP, fill=BOTH)
        self.text_com.insert(END,os.popen('closedisplay').readline())
    def debug(self,event):
        self.root.wm_attributes('-topmost',0)#取消主窗口置顶
        self.w_debug=Toplevel()
        self.w_debug.title('Debug Mode')
        self.w_debug.wm_attributes('-topmost',1)#分窗口置顶
        self.buttonA=Button(self.w_debug,text='Close Display',command=self.tryclose)
        self.buttonA.pack()
        self.buttonB=Button(self.w_debug,text='Close App',command=sys.exit)
        self.buttonB.pack()
        self.buttonC=Button(self.w_debug,text='Shutdown System',command=lambda:os.system('shutdown -s'))
        self.buttonC.pack()
        self.buttonD=Button(self.w_debug,text='Reboot System',command=lambda:os.system('shutdown -r'))
        self.buttonD.pack()
        self.LabelAb=Label(self.w_debug,text='Copyright © 2021 GPL-3.0 WJZ\nPowered by Tkinter on Python\nVersion:V1.4.1')
        self.LabelAb.pack()
    def updatetime(self):
        self.labelE = Label(self.root, text='\n  距离晚自习开始还有：',font = ('黑体' , 75))
        self.labelE.bind_all('<F10>', self.debug)
        self.labelE.pack()
        self.labelF = Label(self.root, text="",font = ('Arial' , 75),fg='red')#空label等待更新
        self.labelF.pack()
        self.labelT = Label(self.root, text="",font = ('Arial' , 25))#空label等待更新
        self.labelT.pack()
        self.labelG = Label(self.root,text=history,font = ('Arial' , font_number))
        self.labelG.pack()
        self.labelH = Label(self.root,text=full_message,font = ('Arial' , 18))
        self.labelH.pack()
        self.updateC()

    def updateC(self):
        # 获取当日日期，不包含时间，str
        self.nowday = datetime.now().strftime("%Y-%m-%d")
        # 字符串拼接，组成当日expect time
        a = self.nowday + ' 18:20:00'
        self.newtime = datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
        t =list(str(self.newtime - datetime.now()))[2:7]#.strftime("%Y-%m-%d %H:%M:%S")#暴力格式化
        self.labelF.configure(text=t)
        # print(t)
        if t == ['0', '0', ':', '0', '0']:
            timetoclose(self.root)#调用函数关闭窗口
            try:
                os.system('closedisplay')
                os.system('shutdown -s -t 1')
            finally:
                sys.exit()
        self.root.after(1000, self.updateC)#1000ms更新倒计时
def showit():
    str_message='''
新华社北京7月24日电 \n近日，中共中央办公厅、国务院办公厅印发了《关于进一步减轻义务教育阶段学生作业负担和校外培训负担的意见》，并发出通知，要求各地区各部门结合实际认真贯彻落实。
'''
    showwarning('Fuck School',str_message)
def timetoclose(window):
    window.destroy()#销毁窗口
if __name__ == '__main__':
    font_number=18
    full_message=''
    if len(str(datetime.now().month))==1:
        month='0'+str(datetime.now().month)
    else:
        month=str(datetime.now().month)
    if len(str(datetime.now().day))==1:
        day='0'+str(datetime.now().day)
    else:
        day=str(datetime.now().day)
    str_date=month+day
    #print(str_date)
    
    try:
        admin_message=requests.get('https://class.api.askdream.top:88/v2/list',headers=headers).json()
        try:
            admin_message=admin_message[str_date]
        except KeyError:
            try:
                data=requests.get('https://www.ipip5.com/today/api.php?type=json',headers=headers).json()['result']
            except:
                history=''
            else:
                for i in range(0,14,2):
                    use_data=data[i]
                    today_message=use_data['year']+'年，'+use_data['title']
                    full_message=full_message+'\n'+today_message
                history='\n\n\n\n历史上的今天'
        else:
            history='\n\n'+admin_message
            font_number=21            
    except:
        history=''
    root = Tk()
    root.title('Fuck School')
    #全屏锁定
    root.attributes('-fullscreen', True)
    #5秒提示
    message2=Label(root,text='\n',font = ('Arial' , 17))
    message2.pack()
    threading.Timer(0.01, timetoclose, args=(message2,)).start()#定时器线程，5s后关闭防沉迷提示
    #倒计时类实例
    TestTime(root)
    #窗口锁定置顶
    root.wm_attributes('-topmost',1)
    #拦截窗口关闭事件
    root.protocol("WM_DELETE_WINDOW",showit)
    #调试button
    #exit_button=Button(root,text='EXIT',command=sys.exit)
    #exit_button.pack()
    #调试结束
    root.mainloop()
