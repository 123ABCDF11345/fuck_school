from tkinter import *
from datetime import datetime
from tkinter.messagebox import *
import sys
import json

class TestTime(object):
    def __init__(self, master=None):
        self.root = master
        self.updatetime()

    def updatetime(self):
        self.labelE = Label(self.root, text='\n  距离str开始还有：',font = ('Arial' , 75))
        self.labelE.bind_all('<Control-Alt-c>', self.exit)#注册快捷键

        self.labelE.pack()
        self.labelF = Label(self.root, text="",font = ('Arial' , 75),fg='red')#空label等待更新
        self.labelF.pack()
        self.labelT = Label(self.root, text="",font = ('Arial' , 25))#空label等待更新
        self.labelT.pack()
        self.updateC()

    def updateC(self):
        # 获取当日日期，不包含时间，str
        self.nowday = datetime.now().strftime("%Y-%m-%d")
        # 字符串拼接，组成当日expect time
        a = self.nowday + ' 20:20:00'
        self.newtime = datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
        t =list(str(self.newtime - datetime.now()))[2:7]#.strftime("%Y-%m-%d %H:%M:%S")#暴力格式化
        self.labelF.configure(text=t)
        self.root.after(1000, self.updateC)
    def exit(self,message):
        if askyesno("GUI-MESSAGEBOX","快捷键捕捉，是否退出?") == True:
            sys.exit()
        else:
            pass


if __name__ == '__main__':
    root = Tk()
    root.title('拯救五班学生于水火之中')
    #全屏锁定
    root.attributes('-fullscreen', True)
    #倒计时类实例
    TestTime(root)
    exit_button=Button(root,text='EXIT',command=sys.exit)
    exit_button.pack()
    root.mainloop()
