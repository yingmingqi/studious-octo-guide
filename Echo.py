# ym
# 格式化输出

# print('{0:{1}^9}\t'.format(ii,chr(12288)),end = '') # 居中对齐
# print('{0:{1}<9}\t'.format(ii,chr(12288)),end = '') # 左对齐    用chr(12288)去填充，即这里的{1}

def Echo(head,body=[]):
   headFormat=[]
   delimiter="    "
   for i,v in enumerate(head):
      leng=len(v)
      for j in body:
         if len(j[i])>leng:
            leng=len(j[i])
      headFormat.append((v,leng))
   def building(string,leng,filler=" "):
      stringlist=[]
      for i,v in enumerate(string):
         stringlist.append(v+filler*(leng[i]-len(v)))
      return stringlist
   
   Format=[k[1] for k in headFormat]
   print(delimiter.join(building(head,Format)))
   print(delimiter.join(building(["-" for i in head], Format, "-")))
   for line in body:
      print(delimiter.join(building(line,Format)))