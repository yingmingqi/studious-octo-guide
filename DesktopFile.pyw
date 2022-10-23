'''

'''

import tkinter as tk
import os, sys
from functools import partial
import configparser


def wirte():
    ncf = configparser.ConfigParser()
    for section in defined:
        for key in defined[section]:
            node = defined[section][key]["node"]
            if node.get('0.0', 'end').strip():
                #print(defined[section][key], node.get('0.0', 'end').strip())
                if section not in ncf.sections(): ncf.add_section(section)
                ncf.set(section, key, node.get('0.0', 'end').strip())

    with open(Path+"\desktop.ini", 'w', encoding='ANSI') as F:
        ncf.write(F)
    
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
                    },
                "{F29F85E0-4FF9-1068-AB91-08002B27B3D9}":{
                        "Prop2":{"name":"标题","text":None,"node":None},
                        "Prop3":{"name":"主题","text":None,"node":None},
                        "Prop4":{"name":"作者","text":None,"node":None},
                        "Prop5":{"name":"标签","text":None,"node":None},
                        "Prop6":{"name":"评论","text":None,"node":None}
                    },
                "{D5CDD502-2E9C-101B-9397-08002B2CF9AE}":{
                        "Prop2":{"name":"类别","text":None,"node":None}
                    },
                "{28636AA6-953D-11D2-B5D6-00C04FD918D0}":{
                        "Prop9":{"name":"类型","text":None,"node":None}
                    },
                "{64440492-4C8B-11D1-8B70-080036B11A03}":{
                        "Prop9":{"name":"评级","text":None,"node":None}
                    }
            }
        
        # UI
        mainWindow = tk.Tk()
        mainWindow.title("Desktop File Edit")
        # 设置窗口大小和位置
        # 500x600   表示窗口大小
        # +2750+300 表示窗口距离电脑屏幕的左边缘和上边缘的距离
        mainWindow.geometry("360x480+2750+300")
        # 禁用缩放
        mainWindow.resizable(False,False)

        #tpath = r"C:\Users\yingm\Desktop\demo\dest" # ceshilujing

        if(os.path.exists(Path+"\desktop.ini")):
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
