import os,sys,json,hashlib,argparse

"""
2019年8月1日16:49:50
"""


"""    版本控制类 链表    """
class LinkedNode(object):
    def __init__(self,Index,Diff,Version=None,Description=None,NextNode=None):
        self.Next = NextNode
        self.Index = Index
        self.Diff = Diff
        self.Version = Version
        self.Description = Description
        
class Version(object):
    def __init__(self,jsondata=None):
        if jsondata:
            self.load(jsondata)
        else:
            self.Head=None
            self.NodeSet=set()

    def load(self,jsondata):
        def serch(index,nodelist):
            for node in nodelist:
                if node.Index==index:
                    return node
            return None
        
        temp=[]
        for dic in jsondata:
            temp.append(LinkedNode( dic["Index"],dic["Diff"],dic["Version"],dic["Description"] ))

        for n in range(len(temp)):
            node, nextnode = serch(n,temp), serch(n+1,temp)
            node.Next=nextnode

        self.Head=serch(0,temp)
        self.NodeSet=set(temp)

    def dump(self,filepath):
        dicts=[]
        temp=self.Head
        while temp:
            dicts.append( {"Index":temp.Index,"Version":temp.Version,"Description":temp.Description,"Diff":temp.Diff} )
            temp=temp.Next

        with open(filepath,"w") as f:
            f.write(json.dumps(dicts,indent=4,separators=(',', ': '),ensure_ascii=False))

    def findHead(self):
        return self.Head

    def findEnd(self):
        temp=self.Head
        while temp:
            if not temp.Next:
                return temp
            temp=temp.Next

    def findNode(self,index):
        temp=self.Head
        while temp:
            if temp.Index==index:
                return temp
            else:
                temp=temp.Next
        return None

    def new(self):
        self.Head=self.newNode({},"initialization","initialization")
        self.NodeSet.add(self.Head)

    def newNode(self,Diff,Version=None,Description=None,nextNode=None):
        Index=0
        node=self.findEnd()
        if node:
            Index=node.Index+1
        return LinkedNode(Index,Diff,Version,Description,nextNode)

    def add(self,node):
        end=self.findEnd()
        end.Next=node
        self.NodeSet.add(node)
    
    
"""    文件信息 多叉树    """
class BranchNode(object):
    def __init__(self, Father, Id, Name):
        self.Father=Father
        self.Id=Id
        self.Name=Name
        self.Children=set()

    def __eq__(self,other):
        return self.Id == other.Id

    def __hash__(self):
        return hash(self.Id)

class LeafNode(BranchNode):
    def __init__(self, Father, Id, Name, Md5):
        self.Father=Father
        self.Id=Id
        self.Name=Name
        self.Md5=Md5
        self.Children=None

class Tree(object):
    def __init__(self):
        self.Root=BranchNode(None,"/","Root")

    def findNode(self,Id,Root=None):
        if not Root:
            Root=self.Root
        findPath=tuple(Id.split("/")[1:])
        fatherNode=Root
        for path in findPath:
            #if not fatherNode.Id+"/"+path in [node.Id for node in fatherNode.Children]:
            if not BranchNode(None,fatherNode.Id+"/"+path,None) in fatherNode.Children:
                return None
            for node in fatherNode.Children:
                if fatherNode.Id+"/"+path==node.Id:
                    fatherNode=node
                    #print(fatherNode.Id)
                    break
        return fatherNode

    def addNode(self,fid,name,md5,children):
        fatherNode=findNode(fid)
        if fatherNode and fatherNode.Children:
            node=LeafNode(fatherNode,fid+"/"+name,name,md5,children)
            fatherNode.Children.add(node)

    def load(self,path):
        Root=BranchNode(None,".","Root")
        folder,file = path[0],path[1]
        
        for f in folder:
            node=Root
            #print("\n")
            for i in tuple(f.split("\\")[1:]):
                newNode=BranchNode(node,node.Id+"/"+i,i)
                if not newNode in node.Children:
                    #print("add",newNode.Id)
                    node.Children.add(newNode)
                    node=newNode
                else:
                    temp=node.Children.copy()
                    while temp:
                        ret=temp.pop()
                        if ret.Id==newNode.Id:
                            node=ret
                            #print("serch",ret.Id)
                            break
                        
        for f in file:
            path,md5=f[0],f[1]
            p,f=os.path.split(path)
            node=self.findNode(p.replace("\\","/"),Root)
            if node:
                node.Children.add(LeafNode(node,node.Id+"/"+f,f,md5))

        self.Root=Root
        #return Root

    def loads(self,jsonfile):
        def buildTree(Node,Dicts):
            for dic in Dicts:
                dic=Dicts[dic]
                if isinstance(dic,dict):
                    Id=dic.get("Id",None)
                    Name=dic.get("Name",None)
                    Md5=dic.get("Md5",None)

                    if Md5:
                        newNode=LeafNode(Node,Id,Name,Md5)
                        Node.Children.add(newNode)
                    else:
                        newNode=BranchNode(Node,Id,Name)
                        Node.Children.add(newNode)
                        buildTree(newNode,dic)
                        
        Node=BranchNode(None,".","Root")
        buildTree(Node,jsonfile)
        return Node

    def dump(self,path):
        def buildDict(Dict,Node):
            children=Node.Children
            if not children:return
            for child in children:
                Dict[child.Name]={"Id":child.Id, "Name":child.Name}
                if child.__dict__.get("Md5",None):
                    Dict[child.Name].update({"Md5":child.Md5})
                buildDict(Dict[child.Name],child)
        Dict={}
        buildDict(Dict,self.Root)

        with open(path,"w") as f:
            f.write(json.dumps(Dict,indent=4,separators=(',', ': '),ensure_ascii=False))
            
        #return json.dumps(Dict)

    def diff(self,A,B):
        def allNode(rootNode):
            nodelist=[]
            def callback(node):
                nodelist.append(node)
                if node.Children:
                    for chaild in node.Children:
                        callback(chaild)
            for chaild in rootNode.Children:
                callback(chaild)
            return nodelist

        def search(Id,List):
            for node in List:
                if node.Id==Id:
                    return node
            return None

        folder,file=[],[]
        partyA=allNode(A)
        partyB=allNode(B)

        for node in partyB:
            onode=search(node.Id,partyA)
            if onode:
                if onode.Id==node.Id and onode.__dict__.get("Md5",None)==node.__dict__.get("Md5",None):
                    partyA.remove(onode)
                else:
                    #C
                    if node.__dict__.get("Md5",None):
                        file.append({"Path":node.Id, "Type":"fe", "Md5":node.Md5, "ADC":"C"})
                    else:
                        folder.append({"Path":node.Id, "Type":"fd", "ADC":"C"})
                    partyA.remove(onode)
            else:
                #A
                if node.__dict__.get("Md5",None):
                    file.append({"Path":node.Id, "Type":"fe", "Md5":node.Md5, "ADC":"A"})
                else:
                    folder.append({"Path":node.Id, "Type":"fd", "ADC":"A"})
                    
        if partyA:
            #D
            for node in partyA:
                if node.__dict__.get("Md5",None):
                    file.append({"Path":node.Id, "Type":"fe", "Md5":node.Md5, "ADC":"D"})
                else:
                    folder.append({"Path":node.Id, "Type":"fd", "ADC":"D"})
                        
        return (folder,file)


"""    Main    """
class Main(object):
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))

        self.fd_cache = os.path.join(self.path,".git","cache")
        self.fd_edition = os.path.join(self.path,".git","edition")
        self.fd_snapshot = os.path.join(self.path,".git","snapshot")
        
        self.fe_config = os.path.join(self.path,".git","config")
        self.fe_filter = os.path.join(self.path,".git","filter")
        self.fe_index = os.path.join(self.path,".git","index")
        self.fe_version = os.path.join(self.path,".git","version")
        if not os.path.exists(self.fe_config):
            self.initialization()
        self.config, self.filter = self.jsonloads(self.fe_config), self.jsonloads(self.fe_filter)

    def initialization(self):
        fd_cache = self.fd_cache
        fd_edition = self.fd_edition
        fd_snapshot = self.fd_snapshot
        
        fe_config = self.fe_config
        fe_filter = self.fe_filter
        fe_index = self.fe_index
        fe_version = self.fe_version
        
        for path in [fd_cache,fd_edition,fd_snapshot]:
            if not os.path.exists(path):
                os.makedirs(path)
            
        js_filter = {"fd":["/.git/*","/__pycache__/*"],"fe":[],"ftype":[".py",".log"]}
        with open(fe_filter,"w") as f:
            f.write(json.dumps(js_filter,indent=4,separators=(',', ': '),ensure_ascii=False))
            
        for file in [fe_config,fe_index]:
            with open(file,"w") as f:
                f.write("{}")

    def jsonloads(self,file):
        js = "{}"
        with open(file,"r") as f:
            js = json.load(f)
        return js

    def scan(self):
        '''
        def get(i,List):
            if len(List)>i:
                return List[i]
            return None
        '''
        def difpath(path):
            def get(i,List):
                if len(List)>i:
                    return List[i]
                return None
            p=path.split("\\")[1:]
            B=True
            for i in filtefd:
                for n in range(len(i)):
                    a, b=i[n], get(n,p)
                    if not a==b and n==0:
                        break
                    if not a==b and n!=0:
                        if a=="*":
                            B=B&False
                        else:
                            B=B&True
            return B
        
        rootPath = self.path
        filters = self.filter
        filtefd = [i.split("/")[1:] for i in filters.get("fd")]
        fdl, fel = [],[]
        if os.path.isdir(rootPath):
            for parent, dirname, filenames in os.walk(rootPath):
                #print(parent,"    =>    ",parent.replace(rootPath,"").replace("\\","/"))
                if parent.replace(rootPath,"") !="" and difpath(parent.replace(rootPath,"")):
                    #print(parent.replace(rootPath,""))
                    fdl.append(parent.replace(rootPath,""))
                for f in filenames:
                    fpath = os.path.join(parent,f)
                    if difpath(parent.replace(rootPath,"")) and os.path.splitext(f)[1] not in filters.get("ftype",[]) and fpath.replace(rootPath,"").replace("\\","/") not in filters.get("fe",[]) :
                        #print(parent,"    =>",f)
                        fel.append((fpath.replace(rootPath,""),self.md5(fpath)))
        return (fdl,fel)

    def md5(self,file):
        with open(file,"rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def copy(self,cmd):
        sys="copy %s %s"%(cmd[0],cmd[1])
        try:
            os.system(sys)
        except Exception as e:
            print(sys,e)

    def backSnapshot(self,Index,filelist):
        fd_snapshot = self.fd_snapshot
        for i in filelist:
            if i.get("ADC")=="D":
                continue
            temp=i.get("Path")
            pathA=os.path.join(self.path,temp.replace("./","").replace("/","\\"))
            pathB=os.path.join(fd_snapshot,str(Index),temp.replace("./","").replace("/","\\"))

            fd=os.path.dirname(pathB)
            if not os.path.exists(fd):
                os.makedirs(fd)
            
            self.copy( (pathA,pathB) )
            

    def backupFile(self,ver,filePath):
        def copy(A,B):
            sys="copy %s %s"%(A,B)
            try:
                os.system(sys)
                #print(sys,"\n")
            except Exception as e:
                print("func[copy] ",e)
                
        rootPath = self.path
        fd_snapshot = self.fd_snapshot
        for dic in filePath:
            if dic.get("ADC") in ["A","C"]:
                path=dic.get("Path")
                fdPath=os.path.join(fd_snapshot,str(ver),"\\".join(path.split("/")[1:-1]))
                filePath=os.path.join(fdPath,path.split("/")[-1])
                if not os.path.exists(fdPath):
                    os.makedirs(fdPath)
                copy(os.path.join(rootPath,"\\".join(path.split("/")[1:])), filePath)

if __name__ == "__main__":
    M=Main()
    T=Tree()
    T.load(M.scan())
    if os.path.exists(M.fe_version):
        V=Version(M.jsonloads(M.fe_version))
    else:
        V=Version()
        V.new()
        V.dump(M.fe_version)

    O=T.loads(M.jsonloads(M.fe_index))
    D=T.diff(O,T.Root)

    """    """
    def Refresh():
        global O
        global D
        T.load(M.scan())
        O=T.loads(M.jsonloads(M.fe_index))
        D=T.diff(O,T.Root)

    """    """
    def Echo(head,body=[]):
        headFormat=[]
        delimiter="    "
        for i,v in enumerate(head):
            leng=len(v)
            for j in body:
                if len(str(j[i]))>leng:
                    leng=len(str(j[i]))
            headFormat.append((v,leng))
        def building(string,leng,filler=" "):
            stringlist=[]
            for i,v in enumerate(string):
                stringlist.append(str(v)+filler*(leng[i]-len(str(v))))
            return stringlist
        Format=[k[1] for k in headFormat]
        print(delimiter.join(building(head,Format)))
        print(delimiter.join(building(["-" for i in head], Format, "-")))
        for line in body:
            print(delimiter.join(building(line,Format)))

    def help():
        print("------还没写")

    def stat(args):
        parser = argparse.ArgumentParser(description='Process some integers.')
        Help="stat [-S|-s|--short]"
        parser.add_argument("-s", "-S", "--short", help=Help, action="store_true")
        
        #arg=parser.parse_args(args)
        arg, unknown=parser.parse_known_args(args)
        if unknown:
            print(Help)
            return
        Refresh()
        
        if arg.short:
            Echo(["fileName","Type","ADC"],[(x.get("Path").split("/")[-1], x.get("Type"), x.get("ADC")) for x in D[0]+D[1]])
        else:
            Echo(["Path","Type","Md5","ADC"],[(x.get("Path"), x.get("Type"), x.get("Md5"," "*32), x.get("ADC")) for x in D[0]+D[1]])

    
    def commit(args):
        parser = argparse.ArgumentParser(description='Process some integers.')
        Help="commit []"
        parser.add_argument("-v", "-V", "--ver", help=Help,default="None")
        parser.add_argument("-d", "-D", "--description", help=Help,default="None")
        arg, unknown=parser.parse_known_args(args)

        if unknown:
            print(Help)
            return
        
        if not D[0]+D[1]:
            print("No Change!")
        else:
            V.add(V.newNode({"fd":D[0],"fe":D[1]}, Version=arg.ver, Description=arg.description))
            V.dump(M.fe_version)
            T.dump(M.fe_index)
            """    备份文件    """
            M.backSnapshot(V.findEnd().Index,D[1])

    def log(args):
        parser = argparse.ArgumentParser(description='Process some integers.')
        Help="log [ 还没写 ]"
        parser.add_argument("-v", "-V", "--ver", help=Help,nargs='+',default=[1],type=int)
        parser.add_argument("-s", "-S", "--short", help=Help, action="store_true")
        arg, unknown=parser.parse_known_args(args)

        def tracks(s,n):
            node=V.findNode(s)
            dic={}
            while node:
                for i in node.Diff.get("fd")+node.Diff.get("fe"):
                    dic[i["Path"]]=(node.Index, i.get("Md5"," "*32), i.get("Type"), i["ADC"], node.Version, node.Description)
                if node.Index==n:
                    break
                else:
                    node=node.Next
            return tuple([(k,v[1],v[2],v[3],v[0],v[4],v[5]) for k,v in dic.items()])

        if unknown:
            print(Help)
            return
        if args:
            #-v -s
            s,e=V.findHead(), V.findEnd()
            if len(arg.ver)==1 and arg.ver[0]<e.Index and arg.ver[0]>0:
                s=V.findNode(arg.ver[0])
            elif len(arg.ver)==2 and arg.ver[1] > arg.ver[0] and (arg.ver[1]+arg.ver[0])/2 < e.Index and arg.ver[0]>0:
                s=V.findNode(arg.ver[0])
                e=V.findNode(arg.ver[1])
            else:
                print(Help)
                return

            History=tracks(s.Index,e.Index)
            
            if arg.short:
                Echo(["File","Type","ADC","Index","Version","Description"],[(x[0].split("/")[-1],x[1],x[2],x[3],x[4],x[5]) for x in History])
            else:
                Echo(["Path","Md5","Type","ADC","Index","Version","Description"],History)
                
        else:
            temp=[]
            Node=V.findHead()
            while Node:
                temp.append((str(Node.Index),Node.Version,Node.Description))
                Node=Node.Next
            Echo(["Index","Version","Description"],temp)
            
    fucnDict={
        "help":help,
        "stat":stat,
        "commit":commit,
        "log":log
        }

    def command(arg):
        args=arg.split()
        if args[0] in ["help","stat","commit","log"]:
            func=fucnDict.get(args[0])
            func(args[1:])
        else:
            help()

    while True:
        command(input())
        print("")
        
