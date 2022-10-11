import math

'''
# 笛卡尔坐标系
给定一个 圆的 中心点 O = (0,0)
给定一个 圆的 半径 r = 16
'''
O = {"x":128,"y":-23}
r = 64

'''
#极坐标系
将 笛卡尔坐标 中心点 O=(0,0) 转换为 极坐标 极点 O
r=16 转为 极经 p=16
Theta 极角 每次旋转 1°
'''

Theta = 0
while Theta < 360:
    M = (r,Theta)

    X = r * math.cos(math.radians(Theta)) + O["x"] #对应坐标修正

    Y = r * math.sin(math.radians(Theta)) + O["y"] #对应坐标修正

    print( "极坐标 M=(%s,%s) => "%M + "笛卡尔坐标 X,Y=(%s,%s)"%( int(X),int(Y) ) )
    
    Theta+=1 #旋转角度
