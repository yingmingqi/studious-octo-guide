# ym
# 拖动文件或文件夹 至 脚本文件 
# 返回文件列表 

import os, sys, re, time, stat

def delFile(fp):
    """ 删除文件
        fp 文件路径
    """
    if os.stat(fp).st_mode == 33060:
        os.chmod(fp,stat.S_IWRITE)#取消只读属性
    os.remove(fp)
    

if __name__ == "__main__":
    """ 在此处处理文件或路径
    """
    element = []
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            element.append(path)
        else:
            for parent, dirname, filenames in os.walk(path):
                for file in filenames:
                    element.append(os.path.join(parent,file))

    # print(element)
    # map(func,element)
    # newList = [fp for fp in element if (fp.split('.')[-1] == 'html')] # 过滤文件

    os.system("pause")