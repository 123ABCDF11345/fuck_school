# Fuck School
**本项目为华夏帝国重点指导项目** 

License:AGPL(GNU AFFERO GENERAL PUBLIC LICENSE)

![AGPL](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2F123ABCDF11345%2Ffuck_school.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2F123ABCDF11345%2Ffuck_school?ref=badge_large)

**最新版本**v1.5.2

### 使用方法 

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

默认表现：
  完整模式 
  禁用日志 
  关闭检测任务管理器进程 
  全屏显示 

注意 
  当使用-z或--zoomed参数时会自动启用--without-full-screen 
  当使用--without-full-screen参数时不会激活zoomed状态 
  当使用-l参数时不会激活--without-full-screen参数 
  当不使用-z或-zoomed或--without-full-screen参数时window-name参数会执行，但屏幕不会出现 

### 项目结构  
- stopclass.py 主程序

技术说明：基于tkinter锁定桌面，显示倒计时；本程序无需除Python3以外的任何依赖项

### 特别声明
- 技术无罪
