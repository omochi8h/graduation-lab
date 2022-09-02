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
import treesimilarity

seitoidentify = ''


class Name(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = QLabel("名前を入力してください", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.move(40,300)

        self.edit = QLineEdit(self)
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(30)
        self.edit.setFont(font)
        self.edit.move(50,350)
        self.edit.setText(seitoidentify)  #ページを戻った時に消えないように


        self.button = QPushButton("進む", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.setGeometry(420, 350, 150, 45)
        self.button.clicked.connect(self.enter)

        self.button = QPushButton("終了", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.setGeometry(425, 775, 250, 100)
        self.button.clicked.connect(QCoreApplication.instance().quit)

    def enter(self):
        global seitoidentify
        seitoidentify = self.edit.text()  #入力を保存
        move(1)




class KadaiList(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.label1 = QLabel('')
        font = QFont()
        font.setPointSize(20)
        self.label1.setFont(font)

        self.label2 = QLabel('　課題を選択してください')
        font = QFont()
        font.setPointSize(17)
        self.label2.setFont(font)

        self.label3 = QLabel('')
        font = QFont()
        font.setPointSize(7)
        self.label3.setFont(font)

        self.label4 = QLabel('')
        font = QFont()
        font.setPointSize(3)
        self.label4.setFont(font)

        self.button = QPushButton("戻る", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.setGeometry(475,800, 200, 70)
        self.button.clicked.connect(self.quit)

        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        list=[]

        c.execute("select kadainame from kadai")
        for i in c:
            list.append(i["kadainame"])

        vbox = [QVBoxLayout(),QVBoxLayout(),QVBoxLayout()]
        hbox = QHBoxLayout()
        line = 0
        for name in list:
            self.button = QPushButton(name)
            self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
            self.button.setStyleSheet("background-color: Gainsboro")
            self.button.clicked.connect(self.kaitou)
            vbox[line].addWidget(self.button)
            vbox[line].addWidget(self.label4)
            line += 1
            if line == 3:
                line = 0

        for v in vbox:
            v.addStretch(1)
            hbox.addLayout(v)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label1)
        vbox2.addWidget(self.label2)
        vbox2.addWidget(self.label3)
        vbox2.addLayout(hbox)
        self.setLayout(vbox2)

    def kaitou(self):
        global kadaiidentify
        b = self.sender()
        kadaiidentify = b.text()  #選択した課題名を他のクラスでも使えるようにする

        #課題名を選択した時点で、学習者が以前にその課題を開いたことがあるか判定する
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #学習者名、課題名で検索
        c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadaiidentify))
        
        jikan = time.time()
        
        if len(c.fetchall()) == 0:  #取得したデータがない
            a = (seitoidentify, kadaiidentify, jikan)  #課題選択の時間を記録。最初のデータを挿入
            c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,similarity,error,judgeparameter,tassei) values(?,?,'','',?,0,1,0,0)", a)

            #実験用データベース
            c.execute("insert into jikken (seitoname,kadainame,sourcecode,output,compiletime,simiold,simijaro,simidice,simited,simito,error) values(?,?,'','',?,0,0,0,0,0,1)", a)
        
        else:  #取得したデータがある
            code = []
            out = []
            ruiji = []
            err = []
            judge = []
            
            c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadaiidentify))
            for i in c:
                code.append(i["sourcecode"])
                out.append(i["output"])
                ruiji.append(i["similarity"])
                err.append(i["error"])
                judge.append(i["judgeparameter"])
            #課題選択の時間を記録。直近のデータを挿入
            a = (seitoidentify, kadaiidentify, code[-1], out[-1], jikan, ruiji[-1], err[-1], judge[-1])
            c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,similarity,error,judgeparameter,tassei) values(?,?,?,?,?,?,?,?,0)", a)

        conn.commit()
        conn.close()

        move(2)

    def quit(self):
        move(0)


class Kaitou(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.label1 = QLabel('課題名 ： ' + str(kadaiidentify))
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)

        self.label2 = QLabel('解答を入力してください')
        font = QFont()
        font.setPointSize(12)
        self.label2.setFont(font)

        self.label3 = QLabel('出力')
        font = QFont()
        font.setPointSize(12)
        self.label3.setFont(font)

        self.edit1 = QTextEdit(self)
        self.edit1.setStyleSheet('background-color: white')
        font = self.edit1.font()  
        font.setPointSize(13)
        self.edit1.setFont(font)

        self.edit2 = linenumber.QCodeEditor(self)
        self.edit2.setStyleSheet('background-color: white')
        font = self.edit2.font()  
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.edit3 = QTextEdit(self)
        self.edit3.setStyleSheet('background-color: white')
        font = self.edit3.font()  
        font.setPointSize(13)
        self.edit3.setFont(font)

        self.button1 = QPushButton("コンパイル・実行", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.clicked.connect(self.compile)

        self.button2 = QPushButton("戻る", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color: Gainsboro")
        self.button2.clicked.connect(self.quit)

        grid = QGridLayout()

        grid.addWidget(self.label1, 0, 0, 1, 2)
        grid.addWidget(self.edit1, 1, 0, 1, 2)

        grid.addWidget(self.label2, 2, 0, 1, 2)
        grid.addWidget(self.edit2, 3, 0, 1, 2)

        grid.addWidget(self.label3, 4, 0, 1, 2)
        grid.addWidget(self.edit3, 5, 0, 1, 2)

        grid.addWidget(self.button1, 6, 0, 1, 1)
        grid.addWidget(self.button2, 6, 1, 1, 1)

        self.setLayout(grid)

        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #クラス内でずっと使えるリスト
        self.code = []
        self.out = []
        self.jikan = []
        self.ruiji = []
        self.err = []
        self.judge = []
        self.mondai = []
        self.answer = []

        c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadaiidentify))
        for i in c:
            self.code.append(i["sourcecode"])
            self.out.append(i["output"])
            self.jikan.append(i["compiletime"])
            self.ruiji.append(i["similarity"])
            self.err.append(i["error"])
            self.judge.append(i["judgeparameter"])

        c.execute("select*from kadai where kadainame=?", (kadaiidentify,))
        for i in c:
            self.mondai.append(i["mondaibun"])
            self.answer.append(i["seikai"])

        self.edit1.setText(self.mondai[-1])
        self.edit2.setPlainText(self.code[-1])
        self.edit3.setPlainText(self.out[-1])

    def compile(self):

        text1 = self.edit2.toPlainText()  #入力ソースコード
        file = open('input.c', 'w', encoding='utf-8')  #writeモードでファイルを開く。input.cがなければ作る。
        file.write(text1)
        file.close()

        text2 = self.answer[-1]  #正解ソースコード
        file = open('answer.c', 'w', encoding='utf-8')  #構文木用に正解ソースコードをファイルにする
        file.write(text2)
        file.close()

        text1 = text1.replace(' ','')  #空白を消す
        text2 = text2.replace(' ','')


        #コンパイル間隔
        jikan = time.time()
        Jikan = jikan - self.jikan[-1]

        #類似度
        #OLD
        import Levenshtein
        
        a = len(text1)
        b = len(text2)
        c = Levenshtein.distance(text1,text2)

        if a > b:
            old = round((1-(c/a)),3)
        else:
            old = round((1-(c/b)),3)

        #Jaro
        import Levenshtein
        a = len(text1)
        b = len(text2)
        c = Levenshtein.jaro(text1,text2)

        jaro = round(c,3)

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
        a = len(text1)
        b = len(text2)
        c = dice.calculate(text1,text2)
        dice = round(c,3)

        #TED，TO
        treesimi = treesimilarity.func()
        ted = treesimi[0]
        to = treesimi[1]
        
        print("old：" + str(old))
        print("jaro：" + str(jaro))
        print("dice：" + str(dice))
        print("ted：" + str(ted))
        print("to：" + str(to))

        #類似度推移（ここになんの類似度を入れるかで使う類似度を設定）
        simi = old
        Ruiji = simi - self.ruiji[-1]

        #プロンプト操作
        e = self.err[-1]
        cmd = ("clang -o input.exe input.c")
        r1 = subprocess.run(cmd.split(),encoding='utf-8',stderr=subprocess.PIPE)  #コンパイルを実行、エラーメッセージを取得

        if r1.returncode == 1:  #コンパイル失敗
            Error = 0.5  #エラー有の判定値倍率
            Out = r1.stderr  #エラー内容
        elif r1.returncode == 0:  #コンパイル成功
            cmd = ("input")
            r2 = subprocess.run(cmd.split(),encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)  #プログラムを実行、出力及びエラーメッセージを取得
            
            if r2.returncode == 1:  #プログラム異常終了
                Out = r2.stderr  #エラー内容
            elif r2.returncode == 0:  #プログラム正常終了
                Out = r2.stdout  #標準出力

            if e == 0.5:  #前回のコンパイルがエラーあり
                Error = 1
            else:  #前回のコンパイルがエラーなし
                Error = e * 1.5

        print("コンパイル間隔：" + str(Jikan))
        print("類似度推移：" + str(Ruiji))
        print("エラー倍率：" + str(Error))
        #判定値
        Judge = round(self.judge[-1] + (pow(Jikan/300, 2) * 1.5 * pow(-Ruiji+1, 3) * Error), 3)
        print("判定値：" + str(Judge))


        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #新しいデータを挿入
        a = (seitoidentify, kadaiidentify, self.edit2.toPlainText(), Out, jikan, simi, Error, Judge)
        c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,similarity,error,judgeparameter,tassei) values(?,?,?,?,?,?,?,?,0)", a)
        conn.commit()

        #実験用データベース
        a = (seitoidentify, kadaiidentify, self.edit2.toPlainText(), Out, jikan, old, jaro, dice, ted, to, Error)
        c.execute("insert into jikken (seitoname,kadainame,sourcecode,output,compiletime,simiold,simijaro,simidice,simited,simito,error) values(?,?,?,?,?,?,?,?,?,?,?)", a)
        conn.commit()

        conn.close()
        move(2)  #画面及びリストを更新

    def quit(self):
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #画面を離れた時点の入力内容を保存
        a = (seitoidentify, kadaiidentify, self.edit2.toPlainText(), self.edit3.toPlainText(), self.jikan[-1], self.ruiji[-1], self.err[-1], self.judge[-1])
        c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,similarity,error,judgeparameter,tassei) values(?,?,?,?,?,?,?,?,0)", a)
        conn.commit()
        conn.close()
        move(1)




class App(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("学生用")
        global tab
        tab = Name(self)
        self.addTab(tab, "Name")
        
        self.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabBar().hide()
        self.resize(700, 900)
        self.move(300,20)
        self.setStyleSheet('background-color:AliceBlue')


def move(page):
    window.removeTab(0)

    if page == 0:
        tab = Name(window)
        window.addTab(tab,"Name")
    elif page == 1:
        tab = KadaiList(window)
        window.addTab(tab,"KadaiList")
    elif page == 2:
        tab = Kaitou(window)
        window.addTab(tab,"Kaitou")

    window.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    global window
    window = App()
    window.show()
    app.exec_()