from tkinter import *
from datetime import datetime
from tkinter.messagebox import *
import sys
import json
import requests
import os
import threading
class TestTime(object):
    def __init__(self, master=None):
        self.root = master
        self.updatetime()

    def updatetime(self):
        self.labelE = Label(self.root, text='\n  距离晚自习开始还有：',font = ('Arial' , 75))
        self.labelE.bind_all('<F9>', self.exit)#注册快捷键

        self.labelE.pack()
        self.labelF = Label(self.root, text="",font = ('Arial' , 75),fg='red')#空label等待更新
        self.labelF.pack()
        self.labelT = Label(self.root, text="",font = ('Arial' , 25))#空label等待更新
        self.labelT.pack()
        self.labelG = Label(self.root,text=history,font = ('Arial' , 18))
        self.labelG.pack()
        self.labelH = Label(self.root,text=full_message,font = ('Arial' , 18))
        self.labelH.pack()
        self.top()
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
            try:
                os.system('shutdown -s -t 1')
            finally:
                sys.exit()
        self.root.after(1000, self.updateC)
    def exit(self,message):
        if askyesno("拖堂防沉迷系统","快捷键捕捉，是否退出?") == True:
            sys.exit()
        else:
            pass
    def top(self):
        self.root.lift()
        self.root.after(50,self.top)#每隔50ms把root窗口置顶
def showit():
    str_message='''
新华社北京7月24日电 \n近日，中共中央办公厅、国务院办公厅印发了《关于进一步减轻义务教育阶段学生作业负担和校外培训负担的意见》，并发出通知，要求各地区各部门结合实际认真贯彻落实。
'''
    showwarning('拖堂防沉迷系统',str_message)
def timetoclose(window):
    window.destroy()
if __name__ == '__main__':
    full_message=''
    admin_message=requests.get('https://class.api.askdream.top:88/note.html')
    admin_message.encoding='utf-8'
    admin_message=admin_message.text
    try:
        if admin_message  != 'display':
            history=admin_message
        else:
            try:
                data=requests.get('https://www.ipip5.com/today/api.php?type=json').json()['result']
            except:
                history=''
            else:
                for i in range(0,14,2):
                    use_data=data[i]
                    today_message=use_data['year']+'年，'+use_data['title']
                    full_message=full_message+'\n'+today_message
                history='\n\n\n\n历史上的今天'
    except:
        history=''
    root = Tk()
    root.title('拯救五班学生于水火之中')
    #全屏锁定
    root.attributes('-fullscreen', True)
    message2=Label(root,text='根据本班最新强化的防沉迷规则，当前时段您不能继续讲课',font = ('Arial' , 17))
    message2.pack()
    threading.Timer(5, timetoclose, args=(message2,)).start()#定时器线程，5s后关闭防沉迷提示
    #倒计时类实例
    TestTime(root)
    root.lift()
    #拦截窗口关闭事件
    root.protocol("WM_DELETE_WINDOW",showit)
    #调试button
#    exit_button=Button(root,text='EXIT',command=sys.exit)
#    exit_button.pack()
    #调试结束
    root.mainloop()
