'''
'''

import tkinter as tk
import os, sys
import configparser
import ctypes


from ctypes import POINTER, Structure, c_int, sizeof, byref
from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR

FCSM_ICONFILE = 0x00000010
FCS_FORCEWRITE = 0x00000002

class GUID(Structure):
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE * 8)]

class SHFOLDERCUSTOMSETTINGS(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwMask', DWORD),
        ('pvid', POINTER(GUID)),
        ('pszWebViewTemplate', LPWSTR),
        ('cchWebViewTemplate', DWORD),
        ('pszWebViewTemplateVersion', LPWSTR),
        ('pszInfoTip', LPWSTR),
        ('cchInfoTip', DWORD),
        ('pclsid', POINTER(GUID)),
        ('dwFlags', DWORD),
        ('pszIconFile', LPWSTR),
        ('cchIconFile', DWORD),
        ('iIconIndex', c_int),
        ('pszLogo', LPWSTR),
        ('cchLogo', DWORD)]


def setInvalidInfo(folderPath):
    """ 写入不完整的 文件夹 图标信息 使资源管理器 强制刷新文件夹信息缓存 """
    fcs = SHFOLDERCUSTOMSETTINGS()
    fcs.dwSize = sizeof(fcs)
    fcs.dwMask = FCSM_ICONFILE

    ctypes.windll.shell32.SHGetSetFolderCustomSettings(byref(fcs), folderPath, FCS_FORCEWRITE)



def wirte():
    ncf = configparser.ConfigParser()
    for section in defined:
        for key in defined[section]:
            node = defined[section][key]["node"]
            if node.get('0.0', 'end').strip():
                #print(defined[section][key], node.get('0.0', 'end').strip())
                if section not in ncf.sections(): ncf.add_section(section)
                ncf.set(section, key, node.get('0.0', 'end').strip())
    try:
        with open(Path+"\desktop.ini", 'w', encoding='ANSI') as F:
            ncf.write(F)
        #ctypes.windll.shell32.SHChangeNotify(0x08000000,0x0000,None,None) # 刷新资源管理器
        #os.system(r"attrib +r "+Path) #添加 文件夹只读属性
        #os.system(r"attrib +s +h "+Path+"\desktop.ini") #添加 文件系统属性/隐藏属性
        hr = setInvalidInfo(Path)
        if hr: ctypes.windll.user32.MessageBoxW(0, "erro", "消息", 10)
        ctypes.windll.user32.MessageBoxW(0, "        写入 desktop.inin 文件，成功！！", "消息", 0)
        
    except:
        ctypes.windll.user32.MessageBoxW(0, "写入失败", "消息", 10)
        
    finally:
        mainWindow.destroy()
        
        
    
def createNode(rot,labelName,value=None):
    lable = tk.Label(rot,text=labelName+"：",anchor="w")

    text = tk.Text(rot,font=('microsoft yahei',9),width=40,height=1)
    text._item = labelName
    if value:
        text.insert('end', value)

    return [lable,text]


if __name__ == "__main__":
    Path = "位置路径"
    if len(sys.argv)==2:
        if not os.path.isdir(sys.argv[1]):
            exit()
        Path = sys.argv[1]

        defined = {
                ".ShellClassInfo":{
                        "infoTip":{"name":"备注","text":None,"node":None}
                        #LocalizedResourceName 设置文件夹别名 显示名称
                    },
                "{F29F85E0-4FF9-1068-AB91-08002B27B3D9}":{
                        "Prop2":{"name":"标题","text":None,"node":None},
                        "Prop3":{"name":"主题","text":None,"node":None},
                        "Prop4":{"name":"作者","text":None,"node":None},
                        "Prop5":{"name":"标记","text":None,"node":None}
                    },
                "{64440492-4C8B-11D1-8B70-080036B11A03}":{
                        "Prop9":{"name":"评级","text":None,"node":None} #数字 1-99
                    },
                "{67DF94DE-0CA7-4D6F-B792-053A3E4F03CF}":{
                        "Prop100":{"name":"标志颜色","text":None,"node":None} #1= Purple,2= Orange,3= Green,4= Yellow,5= Blue,6= Red
                    },
                "{56A3372E-CE9C-11D2-9F0E-006097C686F6}":{
                        "Prop38":{"name":"副标题","text":None,"node":None}
                    }
            }
        
        # UI
        mainWindow = tk.Tk()
        mainWindow.title("Desktop File Edit")
        # 设置窗口大小和位置
        # 500x600   表示窗口大小
        # +2750+300 表示窗口距离电脑屏幕的左边缘和上边缘的距离
        mainWindow.geometry("360x480+800+300")
        # 禁用缩放
        mainWindow.resizable(False,False)

        #tpath = r"C:\Users\yingm\Desktop\demo\dest" # ceshilujing

        if(os.path.exists(Path+"\desktop.ini")):
            os.system(r"attrib "+Path+"\desktop.ini"+" -s -h") #删除 文件系统属性/隐藏属性
            
            cf = configparser.ConfigParser()
            cf.read(Path+"\desktop.ini")
            for section in defined:
                for key in defined[section]:
                    if cf.has_option(section, key):
                        #print(cf.get(section, key), type(cf.get(section, key)), defined[section][key]["name"], "=>", cf.get(section, key))
                        defined[section][key]["text"] = cf.get(section, key)
        else:
            cf = configparser.ConfigParser()
            
        
        div = tk.Frame(mainWindow)

        i = 1
        for section in defined:
            for key in defined[section]:
                p = createNode(div, defined[section][key]["name"], defined[section][key]["text"])
                _label, _input = p
                defined[section][key]["node"] = _input
                _label.grid(row=i, column=0, pady="3", sticky='e')
                _input.grid(row=i, column=1, pady="3")
                
                i+=1

        div.pack(pady="24")
        
        info = tk.Label(mainWindow,text=" "+Path,bg='white',width=360,justify=tk.LEFT,anchor="w")
        info.pack(side="bottom",pady="4")
        
        btn  = tk.Button(mainWindow,text="写入",width=16,command=wirte)
        btn.pack(side="bottom",pady="4")

        # 启动主窗口
        mainWindow.mainloop()
