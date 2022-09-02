import subprocess, re, collections
from functools import reduce
from collections import defaultdict

DIG = []
list_f=[]
list11=[]
list12=[]


def main(name):
    List = []
    if name == "1":
         cmd = ("clang -cc1 -ast-dump answer.c")  #正解ソースコード
         kawawa = "A=("
    elif name == "2":
         cmd = ("clang -cc1 -ast-dump input.c")  #入力ソースコード
         kawawa = "B=("
    i = 0
    I = 0
    String = ''

    runcmd = subprocess.run(cmd.split(),encoding='utf-8',stdout=subprocess.PIPE)
    TXT = runcmd.stdout
    Clang = TXT.split("\n")  #一行ずつの配列にしている
    for c in Clang:
        if I == 0:
            if re.search('FunctionDecl', c) == None:  #まずFunctionDeclが出るまで探す
                pass
            else:
                I = 1  #FunctionDeclが出たら次からelseに行く
                for C in c:  #１文字ずつ？
                    if i == 0:
                        if re.search('[A-Z]', C) == None:  #大文字がないならずっとこっち
                            String = String + C  #１文字ずつ追加？
                        else:
                            String = String + C
                            i = 1  #大文字がでたら次からelifへ(Fが最初に来るはず？)
                    elif i == 1:
                        if re.search('[a-zA-Z]', C) != None:
                            String = String + C  #アルファベットである限り１文字ずつ追加
                        else:
                            i = 2  #アルファベット以外(多分空白)が出た。
                    elif i == 2:
                        break
        else:  #FunctionDecl以下の行
            for C in c:
                if i == 0:
                    if re.search('[A-Z]', C) == None:
                        String = String + C
                    else:
                        String = String + C
                        i = 1
                elif i == 1:
                    if re.search('[a-zA-Z]', C) != None:
                        String = String + C
                    else:
                        i = 2
                elif i == 2:
                    break
        
        #print(String)
        #print(TXT)

        List.append(String)  #なぜリストに追加？
        String = ''
        i = 0
    
    List1 = []
    List2 = []
    for S in List:
        if S != '':
            u=S[1:]  #２文字目以降全てを指定
            List1.append(u)
    
    List1_in_not = [n for n in List1 if "NULL" not in n]
    for y in List1_in_not:
        List2.append(y)
    #print(List2)

    m = ["\|","\-","\`","\x20"]
    M = ["\|*","\-*","\`*","\x20*"]

    B=[]
    C=[]
    b=0
    c=0
    d=0
    line=[]
    kuhaku=[]
    list2 = []
    dict1 = defaultdict(list)
    dict2 = defaultdict(list)
    dict3 = defaultdict(list)
    dict4 = defaultdict(list)
    for a in List2:
        d+=1
        while re.match("[A-Z]",a) == None:
            if re.match("[A-Z]",a) == None:
                if a[0]=="-":
                    A = re.match(M[3],a).end()  #match→先頭が一致するかチェック
                    a = a.lstrip(M[1])
                    dict1.setdefault(d,[]).append(A)
                elif a[0]=="\x20":
                    A = re.match(M[3],a).end()
                    a = a.lstrip(M[3])
                    dict1.setdefault(d,[]).append(A)
                elif a[0]=="`" and a[1]=="-":
                    a = a.lstrip(M[2])
                    a = a.lstrip(M[1])
                elif a[0]=="|" and a[1]=="-":
                    a = a.lstrip(M[0])
                    a = a.lstrip(M[1])
                elif a[0]=="|" and a[1]=="\x20":
                    a = a.lstrip(M[0])
            else:
                break
        else:
            dict2.setdefault(d,a)
            list2.append(a)
    
   #コピーしてるだけ?
    list_a=[]
    for kz in list2:
        list_a.append(kz)

    
    list2_uniq=[]
    
    for ihr in list_a:
        if ihr not in list2_uniq:
            list2_uniq.append(ihr)
    #FunctionDeclとImplicitCastExprが抜けている

    list_b=[]  #つける番号？
    oh=0
    gq=0

    list_c=[]  #コピーしているだけ？
    for iht in list2_uniq:
        indexes = [i for i, x in enumerate(list_a) if x == iht]
        list_b.append(indexes)
        list_c.append(iht)

    
    list2=[]
    ip=0
    oh=1
    lao=0
    gio=0
    dict_jufuku={}
    list_d=[]

    for hgy in list_c:
        dict_jufuku.setdefault(gio,[]).append(hgy)
        gio=gio+1

    hpo=len(list_c)
    for hyu in list_a:
        if hyu not in list_d:
            oh=str(oh)
            ax=hyu+oh
            list2.append(ax)
            list_d.append(hyu)
        else:
            ip=list_d.count(hyu)
            ip=ip+1
            ip=str(ip)
            ax=hyu+ip
            list2.append(ax)
            list_d.append(hyu)
            ip=int(ip)

    eyu=len(list2)
    list_f.append(eyu)
   

    a=''
    A=''
    b=''


    list_moto = []
    for k,v in dict1.items():
        list_moto.append(v)


    def get_unique_list(seq):
        seen = []
        return[x for x in seq if x not in seen and not seen.append(x)]

    uniq1 = []
    for line in list_moto:
        if line not in uniq1:
            uniq1.append(line)

    

    import itertools
    b=0
    d=0
    t=0
    v=0
    r=0
    p=0
    z=0
    z1=0
    number=0
    list1 = []
    list1_1 = []

    list3 = []
    list4 = []
    uniq2 = []
    han="\x20"
    rz="\'\\n   Node ( \"%s\" )' % dict2[d]"
    uniq2=sorted(uniq1)
    
    for a in uniq1:
        d=d+1
        x='\n   Node ( "%s" )\n' % dict2[d]
        l='{}.  addkid ( Node ( "%s" )\n' % dict2[d]
        if len(a)==1:
            list1_1.append(a)
            if number==0:
                list3.append(a)
                list4.append(0)
                number=number+1
            else:
                number=number+1
                t=t+1
                i=4*t
                list3.append(a)
                list4.append(i)
        elif len(a)==2 and r==0:
            r=r+1
            number=number+1
            h=i+4
            list3.append(a)
            list4.append(h)
        elif len(a)==2 and r!=0:
            number=number+1
            h=h+4
            list3.append(a)
            list4.append(h)
        elif len(a)==3 and v==0:
            v=v+1
            number=number+1
            p=h+4
            list3.append(a)
            list4.append(p)
        elif len(a)==3 and v!=0:
            number=number+1
            p=p+4
            list3.append(a)
            list4.append(p)
        elif len(a)==4 and z==0:
            number=number+1
            j=p+4
            list3.append(a)
            list4.append(j)
        elif len(a)==4 and z!=0:
            number=number+1
            j=j+4
            list3.append(a)
            list4.append(j)
        elif len(a)==5 and z1==0:
            number=number+1
            j1=j+4
            list3.append(a)
            list4.append(j1)
        elif len(a)==5 and z1!=0:
            number=number+1
            j1=j1+4
            list3.append(a)
            list4.append(j1)

    b=0
    d=0
    t=0
    v=0
    r=0
    p=0
    z=0
    i=0

    ta=0

    number=0
    list5=[]

    for qa,za in dict1.items():
        list1.append(za)
    
    ir=len(list1)
    list6=[]
               


    for a in list1:
        d=d+1
        if a in list3:
            w=list3.index(a)
            c=list4[w]
            i=list2[z]
            if d==1:
                x='\n   Node ( "%s" )\n'% i
                list5.append(x)
                z=z+1
            else:
                l='{}.  addkid ( Node ( "%s" )\n'% i
                y=l.format(han*c)
                list5.append(y)
                z=z+1
                list6.append(c)

    ty=len(list6)
    
    list11.append(list6)
    list12.append(list2)

    list7=[]
    op=0
    oc=1
    list7.append(0)
    for ky,po in dict1.items():
        if ky!=ty:
            if list6[ky-1]<list6[ky] and oc!=0:
                list7.append(0)
                op=op+1
                oc=oc+1
            elif list6[ky-1]>list6[ky]:
                list7.append(op+1)
                op=0
            elif list6[ky-1]==list6[ky]:
                list7.append(op+1)
                op=0
                oc=0
                oc=oc+1
        else:
            break
    
    if list6[ty-2]<list6[ty-1] and oc!=0:
        list7.append(op+1)
        op=0
        oc=oc+1
    elif list6[ty-2]>list6[ty-1]:
        list7.append(op+1)
        op=0
    elif list6[ty-2]==list6[ty-1]:
        list7.append(op+1)
        op=0
        oc=0
        oc=oc+1
            
    list8=[]
    z=0
    d=0
    it=")"
    for a in list1:
        if a in list3:
            w=list3.index(a)
            c=list4[w]
            i=list2[z]
            if d==0:
                x='\n   Node ( "%s" )\n'% i
                list8.append(x)
                z=z+1
                d=d+1
            else:
                l='{}.  addkid ( Node ( "%s" ){}\n'% i
                y=l.format(han*c,it*list7[d])
                list8.append(y)
                z=z+1
                d=d+1
                        
    list6.insert(0,0)
    p=0
    dig='('
    iy='\''
    fb=','
    np=')'
    bi='('
    list9=[]
    list10=[]
    ew=0
    for a in list6:
        if a==0 and p==0:
            lp=1
            list9.append(list2[p])
            p=p+1
        elif a%4==0 and p!=0:
            if a==4 and lp==1:
                lp=lp+1
                list9.append(list2[p])
                mv=tuple(list9)
                list10.append(mv)
                list9.clear()
                p=p+1
            else:
                hg=list6[p]-4
                while ew<p:
                    if list6[ew]==hg:
                        qs=ew
                        ew=ew+1
                    else:
                        ew=ew+1
                else:
                    list9.append(list2[qs])
                    list9.append(list2[p])
                    mv=tuple(list9)
                    list10.append(mv)
                    list9.clear()
                    p=p+1
                    ew=0
    gp1='['
    gp2=']'
    dig = bi + gp1 + dig[:-1] + gp2 + np
    DIG.append(list10)
            
    s=0
    d=0
    it=")"
    f = open("tree{}.txt".format(name),'w')
    f.write(kawawa)
    for o in list8:
        f.write(o)
    f.close()

    f = open("tree{}.txt".format(name),'a')
    f.write(it)
    f.close()







            
def func():
    try:
        main("1")
        main("2")
    except:
        return ["error", "error"]
    
    from zss import simple_distance , Node
    
    f=open("tree1.txt","r")
    A=(f.read())
    A=Node(A)
    f.close()
    
    f=open("tree2.txt","r")
    B=(f.read())
    B=Node(B)
    f.close()
    

    dig1=DIG[0]
    
    dig2=DIG[1]
    
    import zss
    import networkx as nx
    
    G=nx.DiGraph()
    tree=dig1
    G.add_edges_from(tree)
    T = nx.dfs_tree(G, source='FunctionDecl1')
    nodes_dict1 = {}
    for edge in T.edges():
        if edge[0] not in nodes_dict1:
            nodes_dict1[edge[0]] = zss.Node(edge[0])
        if edge[1] not in nodes_dict1:
            nodes_dict1[edge[1]] = zss.Node(edge[1])
        nodes_dict1[edge[0]].addkid(nodes_dict1[edge[1]])

    H=nx.DiGraph()
    tree=dig2
    H.add_edges_from(tree)
    Y = nx.dfs_tree(H, source='FunctionDecl1')
    nodes_dict = {}
    for edge in Y.edges():
        if edge[0] not in nodes_dict:
            nodes_dict[edge[0]] = zss.Node(edge[0])
        if edge[1] not in nodes_dict:
            nodes_dict[edge[1]] = zss.Node(edge[1])
        nodes_dict[edge[0]].addkid(nodes_dict[edge[1]])

    yatto=zss.simple_distance(nodes_dict1['FunctionDecl1'], nodes_dict['FunctionDecl1'])
    #print(yatto)
    #print(list_f)
    if list_f[1]>list_f[0]:
        ted=round(1-(yatto/list_f[1]),3)
    else:
        ted=round(1-(yatto/list_f[0]),3)


    list13=[]
    list14=[]
    list15=[]
    list16=[]
    list17=[]
    list18=[]
    phi1=0
    htn1=0
    trw1=list_f[0]
    trw2=list_f[1]


    for kqi1 in list11[0]:
        list13.append(kqi1)
        for cep1 in list11[0]:
            list14.append(cep1)
            htn1=htn1+1
            if cep1-kqi1==4 and len(list13)<len(list14):
                list15.append(list14.index(cep1))
            elif kqi1>=cep1 and len(list13)<len(list14):
                ivu1 = list11[0].index(kqi1)
                list15.insert(0,ivu1)
                for biu1 in list15:
                    list16.append(list12[0][biu1])
                if len(list16)==1:
                    break
                else:
                    mojiretu = ''.join(map(str,list16))
                    list17.append(mojiretu)
                    list14.clear()
                    list15.clear()
                    list16.clear()
                    htn1=0
                    break
            elif len(list13)>=len(list14):
                continue
            elif htn1==trw1 and kqi1-cep1==4:
                ivu1 = list11[0].index(kqi1)
                list15.insert(0,ivu1)
                for biu1 in list15:
                    list16.append(list12[0][biu1])
                if len(list16)==1:
                    break
                else:
                    mojiretu = ''.join(map(str,list16))
                    list17.append(mojiretu)
                    list14.clear()
                    list15.clear()
                    list16.clear()
                    htn1=0
                    break
            elif htn1==trw1 and kqi1-cep1!=4:
                ivu1 = list11[0].index(kqi1)
                list15.insert(0,ivu1)
                for biu1 in list15:
                    list16.append(list12[0][biu1])
                if len(list16)==1:
                    break
                else:
                    mojiretu = ''.join(map(str,list16))
                    list17.append(mojiretu)
                    list14.clear()
                    list15.clear()
                    list16.clear()
                    htn1=0
                    break
            else:
                continue

    for lrp1 in list17:
        list18.append(lrp1)
    list13=[]
    list14=[]
    list15=[]
    list16=[]
    list17=[]
    phi1=0
    htn1=0

    for kqi2 in list11[1]:
        list13.append(kqi2)
        for cep2 in list11[1]:
            list14.append(cep2)
            htn1=htn1+1
            if cep2-kqi2==4 and len(list13)<len(list14):
                list15.append(list14.index(cep2))
            elif kqi2>=cep2 and len(list13)<len(list14):
                ivu1 = list11[1].index(kqi2)
                list15.insert(0,ivu1)
                for biu1 in list15:
                    list16.append(list12[1][biu1])
                if len(list16)==1:
                    break
                else:
                    mojiretu = ''.join(map(str,list16))
                    list17.append(mojiretu)
                    list14.clear()
                    list15.clear()
                    list16.clear()
                    htn1=0
                    break
            elif len(list13)>=len(list14):
                continue
            elif htn1==trw2 and kqi2-cep2==4:
                ivu1 = list11[1].index(kqi2)
                list15.insert(0,ivu1)
                for biu1 in list15:
                    list16.append(list12[1][biu1])
                if len(list16)==1:
                    break
                else:
                    mojiretu = ''.join(map(str,list16))
                    list17.append(mojiretu)
                    list14.clear()
                    list15.clear()
                    list16.clear()
                    htn1=0
                    break
            elif htn1==trw2 and kqi2-cep2!=4:
                ivu1 = list11[1].index(kqi2)
                list15.insert(0,ivu1)
                for biu1 in list15:
                    list16.append(list12[1][biu1])
                if len(list16)==1:
                    break
                else:
                    mojiretu = ''.join(map(str,list16))
                    list17.append(mojiretu)
                    list14.clear()
                    list15.clear()
                    list16.clear()
                    htn1=0
                    break
            else:
                continue
        

    icchi=0
    for biq in list17:
        if biq in list18:
            icchi=icchi+1
        else:
            continue

    vpl1=len(list18)
    vpl2=len(list17)
    if vpl2>=vpl1:
        to = round((icchi/vpl2),3)
    else:
        to = round((icchi/vpl1),3)

    return ted,to