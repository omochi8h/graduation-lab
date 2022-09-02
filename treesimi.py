import subprocess, re
from zss import simple_distance, Node


def buildtree(name):
    cmd = ("clang -cc1 -ast-dump {}".format(name))
    r = subprocess.run(cmd.split(),encoding='utf-8',stdout=subprocess.PIPE)
    text = r.stdout
    list1 = text.split("\n")
    list2 = ["root "]

    i = 0
    for line in list1:
        if i == 0:
            if re.search('FunctionDecl', line) != None:
                if re.search('extern', line) != None:
                    pass
                else:
                    list2.append(line)
                    i = 1
        elif i == 1:
            if re.search('extern', line) == None:
                list2.append(line)
            else:
                i = 0

    list3 = []
    dig = []
    for line in list2:
        string = ""
        if "NULL" in line:
            continue
        i = 0
        for index,a in enumerate(line):
            if i == 0:
                if re.search("[a-zA-Z]", a) != None:
                    string = string + a
                    dig.append(int(index/2))
                    i = 1
            elif i == 1:
                if a == " ":
                    string = string.replace("FunctionDecl","関数")
                    string = string.replace("ParamVerDecl","引数")
                    string = string.replace("VarDecl","変数")
                    string = string.replace("RecordDecl","レコード変数")
                    string = string.replace("FieldDecl","フィールド変数")
                    string = string.replace("CompoundStmt","ブロック文")
                    string = string.replace("DeclStmt","変数宣言")
                    string = string.replace("Stmt","")
                    string = string.replace("CStyleCastExpr","キャスト")
                    string = string.replace("ImplicitCastExpr","暗黙キャスト")
                    string = string.replace("CallExpr","関数呼び出し")
                    string = string.replace("DeclRefExpr","変数呼び出し")
                    string = string.replace("BinaryOperator","二項演算子")
                    string = string.replace("UnaryOperator","単項演算子")
                    string = string.replace("InitListExpr","配列式")
                    string = string.replace("ArraySubscriptExpr","配列表現式")
                    string = string.replace("MemberExpr","構造体")
                    string = string.replace("IntegerLiteral","整数")
                    string = string.replace("FloatingLiteral","実数")
                    string = string.replace("StringLiteral","文字列")
                    list3.append(string)
                    break
                else:
                    string = string + a

    """構文木の同一要素に1,2...ってつけるやつ(立花先輩がやってたけど逆効果な気がする)
    for i in set(list3):
        count = 1
        for j in range(len(list3)):
            if i == list3[j]:
                list3[j] = list3[j] + str(count)
                count = count + 1
    """

    bubungi = []
    def partial(index):
        part = [list3[index]]
        partson = []
        for i in range(index+1,len(dig)):
            if dig[i] == dig[index]:
                break
            elif dig[i] == dig[index] + 1:
                partson.append(list3[i])
                partial(i)
        if len(partson) > 0:
            part.append(partson)
            bubungi.append(part)
    partial(0)

    dig.append(1)
    tree = "(\n"
    defaulttree = "(\n"

    for index,node in enumerate(list3):
        tree = tree + "    " * dig[index]
        defaulttree = defaulttree + "    " * dig[index]
        if index != 0:
            tree = tree + ".addkid("
            defaulttree = defaulttree + ".addkid("
        tree = tree + "Node('{}')".format(node) + ")" * (dig[index]-dig[index+1]+1) + "\n"
        defaulttree = defaulttree + "Node('a')" + ")" * (dig[index]-dig[index+1]+1) + "\n"
    tree = tree + ")"
    defaulttree = defaulttree + ")"

    return tree,index+1,bubungi,defaulttree


def func():
    a = buildtree("input.c")
    b = buildtree("answer.c")
    exec("A = {}".format(a[0]),globals())
    exec("B = {}".format(b[0]),globals())
    exec("A1 = {}".format(a[3]),globals())
    exec("B1 = {}".format(b[3]),globals())
    ted0 = simple_distance(A,B)
    ted1 = simple_distance(A1,B1)
    #ted0を木の編集距離の取りうる最大値で割りたい
    #A→Bにするときの最大値は，AとBの構造で一致する部分を「置換」，Aの構造のうちBと一致しない部分を「削除」，Bの構造のうちAと一致しない部分を「挿入」
    #構造が全く同じ木defaulttreeを作って，その間の編集距離を求める(ted1)→これが上の「削除」と「挿入」としていることが一緒
    #a[1]+b[1]-ted1→これが上の「置換」の回数の2倍
    #よって編集距離の最大値は(a[1]+b[1]+ted1)/2
    ted = round(1-(ted0*2/(a[1]+b[1]+ted1)),3)
    #print("解答ソースコード構文木：\n" + str(a[0]))
    #print("解答ソースコード構文木の要素数：" + str(a[1]))
    #print("解答ソースコード構文木の部分木集合：\n" + str(a[2]))
    #print("正解ソースコード構文木：\n" + str(b[0]))
    #print("正解ソースコード構文木の要素数：" + str(b[1]))
    #print("正解ソースコード構文木の部分木集合：\n" + str(b[2]))
    #print("構文木間の編集距離：" + str(ted0))
    #print("TED類似度：" + str(ted))
    to0 = 0
    lena = len(a[2])
    lenb = len(b[2])
    for part in a[2]:
        if part in b[2]:
            b[2].remove(part)
            to0 = to0 + 1
    to = round(1-((lena-to0)+(lenb-to0))/(lena+lenb),3)
    #print("部分木集合間の一致個数：" + str(to0))
    #print("TO類似度：" + str(to))
    return ted, to

#func()