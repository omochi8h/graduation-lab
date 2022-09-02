import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import *

import sqlite3
import time
import linenumber
import subprocess
import treesimi2

seitoidentify = '' #学習者識別用
kadaiidentify = 0 #課題識別用
inp = "" #標準入力（1回コンパイルしたら消えないようにグローバルで宣言）
dbf = "data.db" #データベースファイルの場所


class Login(QWidget): #ログイン画面
    def __init__(self, parent):
        super().__init__(parent)
        label = QLabel("名前を入力してください", self)
        font = QFont()
        font.setPointSize(17)
        label.setFont(font)

        self.edit = QLineEdit(self)
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(30)
        self.edit.setFont(font)

        button = QPushButton("進む", self)
        button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        button.setStyleSheet("background-color: Gainsboro")
        button.clicked.connect(self.enter)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label)
        vbox.addWidget(self.edit)
        vbox.addWidget(button)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def enter(self): #進むボタンで呼び出し
        global seitoidentify
        seitoidentify = self.edit.text() #seitoidentifyを更新
        if seitoidentify == "": #空白のまま進まないように
            message = QMessageBox()
            message.setWindowTitle("警告")
            message.setText("名前を入力してください")
            message.setIcon(QMessageBox.Warning)
            message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
            m = message.exec_()
            return

        #入力内容をデータベースで検索
        conn = sqlite3.connect("{}".format(dbf))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select*from seito where seitoname=?", (seitoidentify,))
        
        if len(c.fetchall()) == 0: #ヒットしなかったら
            message = QMessageBox()
            message.setWindowTitle("確認")
            message.setText("{}さんのデータは存在しません。新しく登録しますか？".format(seitoidentify))
            yesbutton = message.addButton("   はい   ", QMessageBox.ActionRole)
            nobutton = message.addButton("   いいえ   ", QMessageBox.ActionRole)
            message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
            m = message.exec_()

            if message.clickedButton() == yesbutton:
                move(1)
            elif message.clickedButton() == nobutton:
                pass
        else: #ヒットしたら
            move(1)
        conn.close()


class MainWindow(QWidget): #表示画面制御(moveも参照)
    def __init__(self, parent):
        super().__init__(parent)

        window.setWindowTitle("学生用")
        window.resize(1260,900)
        window.move(10,20)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        menu = Menu(self)
        menu.setFrameShape(QFrame.Panel)

        vbox.addWidget(menu)

        if kadaiidentify == 0: #課題が選ばれてないとき
            karappo1 = Karappo1(self)
            karappo1.setFrameShape(QFrame.Panel)
            karappo2 = Karappo2(self)
            karappo2.setFrameShape(QFrame.Panel)
            vbox.addWidget(karappo1)
            hbox.addLayout(vbox)
            hbox.addWidget(karappo2)
        else: #課題が選ばれたとき
            kadaidetail = KadaiDetail(self)
            kadaidetail.setFrameShape(QFrame.Panel)
            kaitou = Kaitou(self)
            kaitou.setFrameShape(QFrame.Panel)
            vbox.addWidget(kadaidetail)
            hbox.addLayout(vbox)
            hbox.addWidget(kaitou)

        self.setLayout(hbox)


class Karappo1(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)


class Karappo2(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)


class Menu(QFrame): #画面左上のメニュー
    def __init__(self, parent=None):
        super().__init__(parent)
        
        label1 = QLabel('名前 ' + seitoidentify)
        font = QFont()
        font.setPointSize(17)
        label1.setFont(font)

        label2 = QLabel('課題を選択してください')
        font = QFont()
        font.setPointSize(17)
        label2.setFont(font)

        button1 = QPushButton("更新", self)
        button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        button1.setStyleSheet("background-color:Gainsboro")
        button1.clicked.connect(self.renew)

        button2 = QPushButton("ログアウト", self)
        button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        button2.setStyleSheet("background-color:Gainsboro")
        button2.clicked.connect(self.logout)

        button3 = QPushButton("終了", self)
        button3.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        button3.setStyleSheet("background-color:Gainsboro")
        button3.clicked.connect(self.syuuryou)

        self.combobox = QComboBox() #課題選択リストボックス
        font = QFont()
        font.setPointSize(17)
        self.combobox.setFont(font)
        self.combobox.setStyleSheet("background-color:white")
        kadailist = ["[達成状況 ☐ or ☑] [課題名]"]
        conn = sqlite3.connect("{}".format(dbf))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select kadainame from kadai")
        for kadai in c:
            kadailist.append(kadai["kadainame"])
        for i in range(1,len(kadailist)): #課題名のそれぞれでデータベース検索し，tasseiの値をとる
            c.execute("select tassei from seito where seitoname=? and kadainame=?", (seitoidentify,kadailist[i]))
            tass = []
            for j in c:
                tass.append(j["tassei"])
            if len(tass) == 0: #まだ選択すらしていない課題
                kadailist[i] = " ☐ " + kadailist[i]
            else: #選択した課題
                if tass[-1] == 0: #直近のtasseiが0
                    kadailist[i] = " ☐ " + kadailist[i]
                elif tass[-1] == 1: #直近のtasseiが1
                    kadailist[i] = " ☑ " + kadailist[i]

        self.combobox.addItems(kadailist)
        self.combobox.setCurrentIndex(kadaiidentify)
        self.combobox.currentIndexChanged.connect(self.kadaisentaku)

        conn.close()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(button1)
        hbox.addWidget(button2)
        hbox.addWidget(button3)
        space = QSpacerItem(100,30,QSizePolicy.Maximum,QSizePolicy.Maximum)
        vbox.addSpacerItem(space)
        vbox.addWidget(label1)
        vbox.addSpacerItem(space)
        vbox.addWidget(label2)
        vbox.addWidget(self.combobox)
        space = QSpacerItem(100,230,QSizePolicy.Maximum,QSizePolicy.Maximum)
        vbox.addSpacerItem(space)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


    def kadaisentaku(self): #リストボックスの変更で呼び出される
        global kadaiidentify
        kadaiidentify = self.combobox.currentIndex() #kadaiidentifyを更新
        if kadaiidentify != 0: #課題が選ばれたとき
            jikan = time.time() #現在時刻を取得
            kadailist = ["No Data"]
            conn = sqlite3.connect("{}".format(dbf))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            #課題リストを作成
            c.execute("select kadainame from kadai")
            for kadai in c:
                kadailist.append(kadai["kadainame"])

            #課題名，学習者名でデータベースを検索
            c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadailist[kadaiidentify]))
        
            if len(c.fetchall()) == 0: #ヒットしなかった（初めて選択した）ら，seitoテーブルに初期値を挿入
                a = (seitoidentify, kadailist[kadaiidentify], jikan)
                c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,simiold,simijaro,simidc,simited,simito,error,judgeparameter,tassei,comp) values(?,?,'','',?,0,0,0,0,0,1,0,0,0)", a)
            else: #ヒットした（以前に選択したことがある）なら，直近の値を取得して，compの値だけ0にして新しいデータを挿入
                code = []
                out = []
                ruijiold = []
                ruijijaro = []
                ruijidc = []
                ruijited = []
                ruijito = []
                err = []
                judge = []
                tass = []
                c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadailist[kadaiidentify]))
                for i in c:
                    code.append(i["sourcecode"])
                    out.append(i["output"])
                    ruijiold.append(i["simiold"])
                    ruijijaro.append(i["simijaro"])
                    ruijidc.append(i["simidc"])
                    ruijited.append(i["simited"])
                    ruijito.append(i["simito"])
                    err.append(i["error"])
                    judge.append(i["judgeparameter"])
                    tass.append(i["tassei"])
                a = (seitoidentify, kadailist[kadaiidentify], code[-1], out[-1], jikan, ruijiold[-1], ruijijaro[-1], ruijidc[-1], ruijited[-1], ruijito[-1], err[-1], judge[-1], tass[-1])
                c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,simiold,simijaro,simidc,simited,simito,error,judgeparameter,tassei,comp) values(?,?,?,?,?,?,?,?,?,?,?,?,?,0)", a)
            conn.commit()
            conn.close()
        move(1)

    def renew(self): #更新
        move(1)

    def logout(self): #ログアウトボタンで呼び出し
        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("ログアウトしますか？")
        yesbutton = message.addButton("   はい   ", QMessageBox.ActionRole)
        nobutton = message.addButton("   いいえ   ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            window.setWindowTitle("ログイン")
            window.resize(400, 300)
            window.move(450,300)
            global seitoidentify, kadaiidentify
            seitoidentify = "" #バグ避け
            kadaiidentify = 0 #バグ避け
            move(0)
        elif message.clickedButton() == nobutton:
            pass

    def syuuryou(self): #終了ボタンで呼び出し
        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("終了しますか？")
        yesbutton = message.addButton("   はい   ", QMessageBox.ActionRole)
        nobutton = message.addButton("   いいえ   ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            QCoreApplication.instance().quit()
        elif message.clickedButton() == nobutton:
            pass


class KadaiDetail(QFrame): #画面左下の表示。問題文と達成
    def __init__(self, parent=None):
        super().__init__(parent)

        label = QLabel('問題文')
        font = QFont()
        font.setPointSize(17)
        label.setFont(font)

        #課題名だけ，問題文だけのリストを作り，そのkadaiidentify番のデータを表示
        self.kadailist = ["No Data"]
        mondaibun = ["No Data"]
        conn = sqlite3.connect("{}".format(dbf))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from kadai")
        for i in c:
            self.kadailist.append(i["kadainame"])
            mondaibun.append(i["mondaibun"])

        edit = QTextEdit()
        edit.setStyleSheet('background-color: white')
        font = edit.font()
        font.setPointSize(13)
        edit.setFont(font)
        edit.setPlainText(mondaibun[kadaiidentify])

        tass = [0,]
        c.execute("select tassei from seito where seitoname=? and kadainame=?", (seitoidentify,self.kadailist[kadaiidentify]))
        for i in c:
            tass.append(i["tassei"])
        self.check = QCheckBox("達成")
        if tass[-1] == 1: #既に達成済みならチェックをつける
            self.check.setChecked(True)
        self.check.clicked.connect(self.achieve)
        self.check.setFont(QtGui.QFont("MS　ゴシック", 17))
        self.check.setStyleSheet("QCheckBox{color: red}")

        conn.close()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)
        vbox.addWidget(edit)
        self.setLayout(vbox)

    def achieve(self): #チェックボックスがクリックされたら呼び出し
        conn = sqlite3.connect("{}".format(dbf))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        a = (seitoidentify,self.kadailist[kadaiidentify])
        if self.check.checkState(): #チェックがつけられたら，tasseiの値を1に更新
            c.execute("update seito set tassei=1,judgeparameter=0 where seitoname=? and kadainame=?", a)
        else: #チェックが外されたら，tasseiの値を0に更新
            c.execute("update seito set tassei=0 where seitoname=? and kadainame=?", a)
        conn.commit()
        conn.close()


class Kaitou(QFrame): #画面右
    def __init__(self, parent=None):
        super().__init__(parent)

        #非同期処理（ちょっと難しい）
        #コンパイルや類似度計算の動作が重いので，実行ボタンがちゃんと押されたかどうかのフィードバックが欲しい。
        #類似度などの処理をしている間，実行ボタンを消してloading・・・と表示する。
        #しかし，pythonはある命令をしたときその命令の全てが終わってから画面を更新する(同期的)ので実行ボタンを押してもloadingが表示されない。
        #そこで，pythonに同時に2つの処理をさせて，片方が終わった際に画面が更新されるようにする。（マルチスレッド化）
        #loadingの表示の処理をメインスレッド，類似度などの重い処理をする関数をサブスレッドで行う。
        class Worker(QObject): #重い処理。これをサブスレッドに入れる。
            finished = pyqtSignal() #シグナルを宣言
            edit1 = linenumber.QCodeEditor()
            edit3 = linenumber.QCodeEditor()
            kadailist = ["No Data"]
            answer = []
            jikan = []
            ruijiold = []
            ruijijaro = []
            ruijidc = []
            ruijited = []
            ruijito = []
            err = []
            judge = []
            tass = [0]

            def run(self): #コンパイルと類似度計算
                conn = sqlite3.connect("{}".format(dbf))
                conn.row_factory = sqlite3.Row
                c = conn.cursor()

                global inp
                inp = self.edit3.toPlainText() #標準入力

                text1 = self.edit1.toPlainText() #解答ソースコード
                file = open('input.c', 'w', encoding='utf-8') #.cファイルに出力
                file.write(text1)
                file.close()

                text2 = self.answer[-1] #正解ソースコード
                file = open('answer.c', 'w', encoding='utf-8')
                file.write(text2)
                file.close()

                #コメント文を消す
                while text1.count("//")>0:
                    for i in range(text1.find("//"),len(text1)):
                        if text1[i]=="\n":
                            text1 = text1[:text1.find("//")] + text1[i+1:]
                            break
                        elif i == len(text1)-1:
                            text1 = text1[:text1.find("//")]
                while text1.count("/*")>0 and text1.count("*/")>0:
                    text1 = text1[:text1.find("/*")] + text1[text1.find("*/")+2:]
                while text2.count("//")>0:
                    for i in range(text2.find("//"),len(text2)):
                        if text2[i]=="\n":
                            text2 = text2[:text2.find("//")] + text2[i+1:]
                            break
                        elif i == len(text2)-1:
                            text2 = text2[:text2.find("//")]
                while text2.count("/*")>0 and text2.count("*/")>0:
                    text2 = text2[:text2.find("/*")] + text2[text2.find("*/")+2:]

                #空白，改行を消す
                text1 = text1.replace(' ','')
                text2 = text2.replace(' ','')
                text1 = text1.replace('\n','')
                text2 = text2.replace('\n','')
                #インデントの削除
                text1 = text1.replace('	','')
                text2 = text2.replace('	','')             
                print(text2)

                #コンパイル間隔
                jikan = time.time()
                Jikan = jikan - self.jikan[-1]

                #類似度
                #OLD
                import Levenshtein
        
                a = len(text1)
                b = len(text2)
                d = Levenshtein.distance(text1,text2)

                if a > b:
                    old = round((1-(d/a)),3)
                else:
                    old = round((1-(d/b)),3)

                #Jaro
                d = Levenshtein.jaro(text1,text2)
                jaro = round(d,3)

                #Dice
                from pysummarization.similarity_filter import SimilarityFilter

                class Dice(SimilarityFilter):
                    def calculate(self, str1, str2):
                        x, y = self.unique(str1, str2)
                        try:
                            result = 2 * len(x & y) / float(sum(map(len, (x, y))))
                        except ZeroDivisionError:
                            result = 0.0
                        return result

                dice = Dice()
                d = dice.calculate(text1,text2)
                dc = round(d,3)

                # Simpson
                class Simpson(SimilarityFilter):
                    def calculate(self, str1, str2):
                        x, y = self.unique(str1, str2)
                        try:
                            result = len(x & y) / float(min(map(len, (x, y))))
                        except ZeroDivisionError:
                            result = 0.0
                        return result

                simpson = Simpson()
                d = simpson.calculate(text1,text2)
                sc = round(d,3)

                #TED，TO
                try:
                    tree = treesimi2.func()
                except: #例外処理
                    tree = [0,0]
                ted = tree[0]
                to = tree[1]
        
                print("old：" + str(old))
                print("jaro：" + str(jaro))
                print("dice：" + str(dc))
                print("simpson：" + str(sc))
                print("ted：" + str(ted))
                print("to：" + str(to))

                #類似度推移（ここになんの類似度を入れるかで使う類似度を設定。教員用SeitoDetail,scrolltableも一緒に変えること）
                Ruiji = old - self.ruijiold[-1]

                #プロンプト操作
                e = self.err[-1]
                cmd = ("clang -o input.exe input.c")
                r1 = subprocess.run(cmd.split(),input=inp,encoding='utf-8',stderr=subprocess.PIPE)  #コンパイルを実行、エラーメッセージを取得

                if r1.returncode == 1:  #コンパイル失敗
                    Error = 0.5
                    Out = r1.stderr  #エラー内容
                elif r1.returncode == 0:  #コンパイル成功
                    cmd = ("input")
                    try:
                        r2 = subprocess.run(cmd.split(),input=inp,encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)  #プログラムを実行、出力及びエラーメッセージを取得
                    except:
                        pass
                    Out = "予期せぬエラーが起きたようです。" #プログラム実行エラーとか，ctrl-cとか

                    if r2.returncode == 1:  #プログラム異常終了
                        Out = r2.stderr  #エラー内容
                    elif r2.returncode == 0:  #プログラム正常終了
                        Out = r2.stdout  #標準出力

                    if e == 0.5:  #前回のコンパイルがエラーあり
                        Error = 1
                    else:  #前回のコンパイルがエラーなし
                        Error = e * 1.5

                #print("コンパイル間隔：" + str(Jikan))
                #print("類似度推移：" + str(Ruiji))
                #print("エラー倍率：" + str(Error))
                
                #躓き度の指標(使わない)
                Judge = round(self.judge[-1] + (pow(Jikan/300, 2) * 1.5 * pow(-Ruiji+1, 3) * Error), 3)
                #print("判定値：" + str(Judge))

                #新しいデータを挿入
                a = (seitoidentify, self.kadailist[kadaiidentify], self.edit1.toPlainText(), Out, jikan, old,jaro,dc,ted,to, Error, Judge, self.tass[-1])
                c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,simiold,simijaro,simidc,simited,simito,error,judgeparameter,tassei,comp) values(?,?,?,?,?,?,?,?,?,?,?,?,?,1)", a)
                conn.commit()
                conn.close()
                self.finished.emit() #終わりを示すシグナルを放出する

        self.w = Worker() #Workerクラスをインスタンス化。Workerクラスの変数が使えるようになる。

        label1 = QLabel('解答を入力してください')
        font = QFont()
        font.setPointSize(17)
        label1.setFont(font)

        self.check1 = QCheckBox('出力')
        font = QFont()
        font.setPointSize(17)
        self.check1.setFont(font)
        self.check1.setChecked(True)
        self.check1.clicked.connect(self.syutsuryoku)
        self.check1.setFont(QtGui.QFont("MS　ゴシック", 17))

        self.check2 = QCheckBox('入力(ある場合)')
        font = QFont()
        font.setPointSize(17)
        self.check2.setFont(font)
        self.check2.clicked.connect(self.nyuuryoku)
        self.check2.setFont(QtGui.QFont("MS　ゴシック", 17))

        self.label2 = QLabel('Loading・・・')
        font = QFont()
        font.setPointSize(29)
        self.label2.setFont(font)
        self.label2.setAlignment(Qt.AlignCenter)

        self.w.edit1.setStyleSheet('background-color: white')
        font = self.w.edit1.font()  
        font.setPointSize(13)
        self.w.edit1.setFont(font)

        self.edit2 = QTextEdit(self)
        self.edit2.setStyleSheet('background-color: white')
        font = self.edit2.font()
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.w.edit3.setStyleSheet('background-color: white')
        font = self.w.edit3.font()  
        font.setPointSize(13)
        self.w.edit3.setFont(font)
        self.w.edit3.setPlainText(inp)

        self.button = QPushButton("コンパイル・実行", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 23, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.clicked.connect(self.compile)

        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(self.w.edit1)
        vbox.addWidget(self.check1)
        vbox.addWidget(self.edit2)
        vbox.addWidget(self.check2)
        vbox.addWidget(self.w.edit3)
        vbox.addWidget(self.button)
        vbox.addWidget(self.label2)
        self.setLayout(vbox)
        self.w.edit3.hide()
        self.label2.hide()

        #これらはWorkerクラスで使わないのでこちらで宣言
        self.code = []
        self.out = []
        self.mondai = []
        self.template = []
        
        
        conn = sqlite3.connect("{}".format(dbf))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from kadai")
        for i in c:
            self.w.kadailist.append(i["kadainame"]) #課題リスト作成

        #学習者名，課題名で検索
        c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,self.w.kadailist[kadaiidentify]))
        for i in c:
            self.code.append(i["sourcecode"])
            self.out.append(i["output"])
            self.w.jikan.append(i["compiletime"])
            self.w.ruijiold.append(i["simiold"])
            self.w.ruijijaro.append(i["simijaro"])
            self.w.ruijidc.append(i["simidc"])
            self.w.ruijited.append(i["simited"])
            self.w.ruijito.append(i["simito"])
            self.w.err.append(i["error"])
            self.w.judge.append(i["judgeparameter"])
            self.w.tass.append(i["tassei"])

        c.execute("select*from kadai where kadainame=?", (self.w.kadailist[kadaiidentify],))
        for i in c:
            self.w.answer.append(i["seikai"])
            self.template.append(i["template"])

        conn.close()
        if self.code[-1] == "": #解答ソースコードが空白(コンパイルしてない)ならひな型を表示
            self.w.edit1.setPlainText(self.template[-1])
        else: #以前書いたソースコードがあればそちらを表示
            self.w.edit1.setPlainText(self.code[-1])
        self.edit2.setPlainText(self.out[-1]) #出力結果を表示

    def compile(self): #コンパイル・実行ボタンで呼び出される(メインスレッド)
        self.thread = QThread() #新しいスレッドを宣言
        self.w.moveToThread(self.thread) #Workerクラスをサブスレッドに移動
        self.thread.started.connect(self.w.run) #サブスレッドがスタートしたらrunを実行

        #サブスレッドを終了するやつら。詳しいことは知らない
        self.w.finished.connect(self.thread.quit)
        self.w.finished.connect(self.w.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.finished.connect(self.renew) #処理が終わったら(finishedシグナルを受け取ったら)画面更新
        self.thread.start() #サブスレッドをスタート
        self.button.hide() #実行ボタンを隠す
        self.label2.show() #loadingを表示

    def syutsuryoku(self): #出力欄の表示切り替え操作
        if self.check1.checkState():
            self.edit2.show()
        else:
            self.edit2.hide()

    def nyuuryoku(self): #入力欄の表示切り替え操作
        if self.check2.checkState():
            self.w.edit3.show()
        else:
            self.w.edit3.hide()

    def renew(self): #更新
        try:
            move(1)
        except KeyboardInterrupt: #学生が無限ループのプログラムを作ってしまったときctrl-cで抜け出しても大丈夫なように
            move(1)


class App(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ログイン")
        global tab
        tab = Login(self)
        self.addTab(tab, "ログイン")
        
        self.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.resize(400, 300)
        self.tabBar().hide()
        self.move(450,300)
        self.setStyleSheet('background-color:AliceBlue')


def move(page):
    window.removeTab(0)

    if page == 0:
        tab = Login(window)
        window.addTab(tab,"Name")
    elif page == 1:
        tab = MainWindow(window)
        window.addTab(tab,"MainWindow")

    window.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    global window
    window = App()
    window.show()
    app.exec_()