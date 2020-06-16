# ym
# 拖动文件或文件夹 至 脚本文件 
# 返回文件列表 

import os, sys, re, time, stat

def delFile(f=None,fl=None,fn=[],ft=[]):
    """ 删除文件
        f  文件路径
        fl 文件路径列表
        fn 符合删除条件的文件名
        ft 符合删除条件的文件类型
    """
    def delete(fp):
        if os.stat(fp).st_mode == 33060:
            os.chmod(fp,stat.S_IWRITE)#取消只读属性
        os.remove(fp)
    
    if f and (os.path.splitext(os.path.split(f)[1])[0] in fn or os.path.splitext(os.path.split(f)[1])[0] in ft):
        print("del - %s"%f)
        delete(f)
    if fl:
        for f in fl:
            if f and (os.path.splitext(os.path.split(f)[1])[0] in fn or os.path.splitext(os.path.split(f)[1])[0] in ft):
                print("del - %s"%f)
                delete(f)


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

    os.system("pause")