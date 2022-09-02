import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import *

import sqlite3
import time
import linenumber


kiiro = "20"


class Menu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.button = QPushButton("課題リスト", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.setGeometry(100, 300, 200, 200)
        self.button.clicked.connect(self.kadailist)

        self.button = QPushButton("学習者リスト", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.setGeometry(400, 300, 200, 200)
        self.button.clicked.connect(self.seitolist)

        self.button = QPushButton("終了", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.setGeometry(425, 775, 250, 100)
        self.button.clicked.connect(QCoreApplication.instance().quit)


    def kadailist(self):
        move(1)

    def seitolist(self):
        move(2)


class KadaiList(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.label1 = QLabel('')
        font = QFont()
        font.setPointSize(20)
        self.label1.setFont(font)

        self.label2 = QLabel('　課題の閲覧・編集・削除ができます')
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

        self.button = QPushButton("新規課題保存", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color: Gainsboro")
        self.button.setGeometry(25, 800, 400, 70)
        self.button.clicked.connect(self.kadaihozon)

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
        line = 0  #列を決定
        for count, name in enumerate(list):
            self.button = QPushButton(name)
            self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
            self.button.setStyleSheet("background-color: Gainsboro")
            self.button.index = count
            self.button.clicked.connect(self.kadaidetail)
            vbox[line].addWidget(self.button)
            vbox[line].addWidget(self.label4)
            line += 1
            if line == 3:
                line = 0

        for v in vbox:
            v.addStretch(1)
            hbox.addLayout(v)  #縦に並べたボタンを横に並べる

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label1)
        vbox2.addWidget(self.label2)
        vbox2.addWidget(self.label3)
        vbox2.addLayout(hbox)
        self.setLayout(vbox2)

    def kadaidetail(self):
        global kadaiidentify1
        b = self.sender()
        kadaiidentify1 = b.index  #選んだ課題のインデックス値を他のクラスでも使える
        move(4)

    def kadaihozon(self):
        move(3)

    def quit(self):
        move(0)


class SeitoList(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.button1 = QPushButton("更新", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.setGeometry(25, 800, 312, 70)
        self.button1.clicked.connect(self.upd)

        self.button2 = QPushButton("戻る", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color: Gainsboro")
        self.button2.setGeometry(363, 800, 312, 70)
        self.button2.clicked.connect(self.quit)

        #レイアウトの影響でラベルが勝手に小さくなって文字が途中で途切れるので細かく区切って表示
        self.label = QLabel("分間コ", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.move(160,750)

        self.label = QLabel("ンパイル", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.move(223,750)

        self.label = QLabel("がない", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.move(296,750)

        self.label = QLabel("学習者", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.move(355,750)

        self.label = QLabel("を黄色", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.move(424,750)

        self.label = QLabel("で表示", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.move(486,750)

        self.edit = QLineEdit(self)
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(25)
        self.edit.setFont(font)
        self.edit.move(50,750)
        self.edit.setText(kiiro)  #黄色表示の秒数


        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        seitoset = set()  #学習者名の配列(被りなし)

        c.execute("select seitoname from seito")
        for i in c:
            seitoset.add(i["seitoname"])
            
        vbox = [QVBoxLayout(),QVBoxLayout(),QVBoxLayout()]
        hbox = QHBoxLayout()
        line = 0

        for seito in sorted(seitoset):
            kadai = []
            judge = []
            jikan = []

            c.execute("select*from seito where seitoname=?", (seito,))
            for i in c:
                kadai.append(i["kadainame"])
                jikan.append(i["compiletime"])
                judge.append(i["judgeparameter"])

            name = seito + "\n" + kadai[-1] + "\n判定値：" + str(round(judge[-1], 3))  #各学習者の直近のデータ
            self.button = QPushButton(name)
            self.button.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))

            if judge[-1] >= 3:
                self.button.setStyleSheet("background-color: red")
            elif (time.time()-jikan[-1]) >= int(self.edit.text())*60:  #現在時刻－前回のコンパイル >= kiiro×60
                self.button.setStyleSheet("background-color: Yellow")
            else:
                self.button.setStyleSheet("background-color: Gainsboro")

            self.button.index1 = seito
            self.button.index2 = kadai[-1]
            self.button.clicked.connect(self.seitodetail)
            vbox[line].addWidget(self.button)
            line += 1
            if line == 3:
                line = 0

        for v in vbox:
            v.addStretch(1)
            hbox.addLayout(v)

        self.setLayout(hbox)
        

    def seitodetail(self):
        global seitoidentify
        global kadaiidentify2
        b = self.sender()
        seitoidentify = b.index1  #選択した学習者名、
        kadaiidentify2 = b.index2  #選択した課題名を他のクラスでも使える
        move(5)

    def upd(self):
        global kiiro

        #kiiroに数字以外を入力してもエラーが起きないようにする
        try:
            int(self.edit.text())
        except:  #tryに失敗
            message = QMessageBox()
            message.setWindowTitle("失敗")
            message.setText("数字のみで入力してください")
            okbutton = message.addButton("OK", QMessageBox.AcceptRole)
            message.setDefaultButton(okbutton)
            m = message.exec_()
        else:  #tryが正常終了
            kiiro = self.edit.text()
            move(2)  #更新

    def quit(self):
        move(0)


class KadaiHozon(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.button1 = QPushButton("保存", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.clicked.connect(self.save)

        self.button2 = QPushButton("戻る", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color: Gainsboro")
        self.button2.clicked.connect(self.quit)

        self.label1 = QLabel('課題名を入力してください（他の課題名と被らないようにしてください）')
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)

        self.label2 = QLabel('問題文を入力してください')
        font = QFont()
        font.setPointSize(12)
        self.label2.setFont(font)

        self.label3 = QLabel('正解ソースコードを入力してください')
        font = QFont()
        font.setPointSize(12)
        self.label3.setFont(font)


        self.edit1 = QLineEdit(self)
        self.edit1.setStyleSheet('background-color: white')
        font = self.edit1.font()  
        font.setPointSize(13)
        self.edit1.setFont(font)

        self.edit2 = QTextEdit(self)
        self.edit2.setStyleSheet('background-color: white')
        font = self.edit2.font()  
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.edit3 = QTextEdit(self)
        self.edit3.setStyleSheet('background-color: white')
        font = self.edit3.font()  
        font.setPointSize(13)
        self.edit3.setFont(font)

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

    def save(self):
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        self.Text1 = self.edit1.text()
        self.Text2 = self.edit2.toPlainText()
        self.Text3 = self.edit3.toPlainText()
        a = (self.Text1, self.Text2, self.Text3)

        c.execute("insert into kadai(kadainame,mondaibun,seikai) values(?,?,?)", a)
        conn.commit()
        conn.close()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("保存しました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setDetailedText(self.Text1 + '\n\n' + self.Text2 + '\n\n' + self.Text3)
        m = message.exec_()
        

    def quit(self):
        move(1)


class KadaiDetail(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.button1 = QPushButton("編集", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.clicked.connect(self.save)

        self.button2 = QPushButton("課題削除", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color: Gainsboro")
        self.button2.clicked.connect(self.delete)

        self.button3 = QPushButton("戻る", self)
        self.button3.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button3.setStyleSheet("background-color: Gainsboro")
        self.button3.clicked.connect(self.quit)

        self.label1 = QLabel('課題名（他の課題名と被らないようにしてください）')
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)

        self.label2 = QLabel('問題文')
        font = QFont()
        font.setPointSize(12)
        self.label2.setFont(font)

        self.label3 = QLabel('正解ソースコード')
        font = QFont()
        font.setPointSize(12)
        self.label3.setFont(font)

        self.edit1 = QLineEdit(self)
        self.edit1.setStyleSheet('background-color: white')
        font = self.edit1.font()  
        font.setPointSize(13)
        self.edit1.setFont(font)

        self.edit2 = QTextEdit(self)
        self.edit2.setStyleSheet('background-color: white')
        font = self.edit2.font()  
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.edit3 = QTextEdit(self)
        self.edit3.setStyleSheet('background-color: white')
        font = self.edit3.font()
        font.setPointSize(13)
        self.edit3.setFont(font)

        grid = QGridLayout()

        grid.addWidget(self.label1, 0, 0, 1, 3)
        grid.addWidget(self.edit1, 1, 0, 1, 3)

        grid.addWidget(self.label2, 2, 0, 1, 3)
        grid.addWidget(self.edit2, 3, 0, 1, 3)

        grid.addWidget(self.label3, 4, 0, 1, 3)
        grid.addWidget(self.edit3, 5, 0, 1, 3)

        grid.addWidget(self.button1, 6, 0, 1, 1)
        grid.addWidget(self.button2, 6, 1, 1, 1)
        grid.addWidget(self.button3, 6, 2, 1, 1)

        self.setLayout(grid)


        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        list1=[]
        list2=[]
        list3=[]

        c.execute("select*from kadai")
        for i in c:
            list1.append((i["kadainame"]))
            list2.append((i["mondaibun"]))
            list3.append((i["seikai"]))

        conn.close()

        self.text1 = list1[kadaiidentify1]
        self.text2 = list2[kadaiidentify1]
        self.text3 = list3[kadaiidentify1]

        self.edit1.setText(self.text1)
        self.edit2.setPlainText(self.text2)
        self.edit3.setPlainText(self.text3)
        

    def save(self):
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        self.Text1 = self.edit1.text()
        self.Text2 = self.edit2.toPlainText()
        self.Text3 = self.edit3.toPlainText()
        a = (self.Text1, self.Text2, self.Text3, self.text1)

        c.execute("update kadai set kadainame=?,mondaibun=?,seikai=? where kadainame=?", a)
        conn.commit()
        conn.close()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("編集しました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setDetailedText(self.Text1 + '\n\n' + self.Text2 + '\n\n' + self.Text3)
        m = message.exec_()


    def delete(self):

        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("本当に削除しますか？")
        yesbutton = message.addButton("はい", QMessageBox.ActionRole)
        nobutton = message.addButton("いいえ", QMessageBox.ActionRole)
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("delete from kadai where kadainame=?", (self.text1,))
            conn.commit()
            conn.close()
            move(1)
        elif message.clickedButton() == nobutton:
            pass
        

    def quit(self):
        move(1)


class SeitoDetail(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        self.code = []
        self.out = []
        self.jikan = []
        self.ruiji = []
        self.err = []
        self.judge = []

        c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadaiidentify2))
        for i in c:
            self.code.append(i["sourcecode"])
            self.out.append(i["output"])
            self.jikan.append(i["compiletime"])
            self.ruiji.append(i["similarity"])
            self.err.append(i["error"])
            self.judge.append(i["judgeparameter"])

        self.label1 = QLabel("学習者名 ： " + str(seitoidentify), self)
        font = QFont()
        font.setPointSize(13)
        self.label1.setFont(font)

        self.label2 = QLabel("課題名 ： " + str(kadaiidentify2), self)
        font = QFont()
        font.setPointSize(13)
        self.label2.setFont(font)

        self.label3 = QLabel("類似度 ： " + str(self.ruiji[-1]), self)
        font = QFont()
        font.setPointSize(13)
        self.label3.setFont(font)

        self.label4 = QLabel("判定値 ： " + str(round(self.judge[-1], 3)), self)
        font = QFont()
        font.setPointSize(13)
        self.label4.setFont(font)

        self.label5 = QLabel("最後のコンパイル時間 ： " + str(round((time.time()-self.jikan[-1])/60)) + "分前", self)
        font = QFont()
        font.setPointSize(13)
        self.label5.setFont(font)

        self.label6 = QLabel("ソースコード", self)
        font = QFont()
        font.setPointSize(13)
        self.label6.setFont(font)

        self.label7 = QLabel("出力", self)
        font = QFont()
        font.setPointSize(13)
        self.label7.setFont(font)

        self.edit1 = linenumber.QCodeEditor(self)
        self.edit1.setStyleSheet('background-color: white')
        font = self.edit1.font()  
        font.setPointSize(13)
        self.edit1.setFont(font)

        self.edit2 = QTextEdit(self)
        self.edit2.setStyleSheet('background-color: white')
        font = self.edit2.font()  
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.button1 = QPushButton("判定値リセット", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.clicked.connect(self.reset)
        
        self.button2 = QPushButton("学習者削除", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color: Gainsboro")
        self.button2.clicked.connect(self.delete)

        self.button3 = QPushButton("戻る", self)
        self.button3.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button3.setStyleSheet("background-color: Gainsboro")
        self.button3.clicked.connect(self.quit)

        self.button4 = QPushButton("学習者", self)
        self.button4.setFont(QtGui.QFont("MS　ゴシック", 13, QFont.Medium))
        self.button4.setStyleSheet("background-color: Gainsboro")
        self.button4.clicked.connect(self.seitosource)
        self.button4.setGeometry(470,72,100,25)

        self.button5 = QPushButton("正解", self)
        self.button5.setFont(QtGui.QFont("MS　ゴシック", 13, QFont.Medium))
        self.button5.setStyleSheet("background-color: Gainsboro")
        self.button5.clicked.connect(self.seikaisource)
        self.button5.setGeometry(580,72,100,25)

        self.button6 = QPushButton("他の課題", self)
        self.button6.setFont(QtGui.QFont("MS　ゴシック", 13, QFont.Medium))
        self.button6.setStyleSheet("background-color: Gainsboro")
        self.button6.clicked.connect(self.another)
        self.button6.setGeometry(580,5,100,25)

        self.edit1.setPlainText(self.code[-1])
        self.edit2.setPlainText(self.out[-1])

        hbox = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]
        vbox = QVBoxLayout()

        hbox[0].addWidget(self.label1)
        hbox[0].addWidget(self.label2)
        hbox[1].addWidget(self.label3)
        hbox[1].addWidget(self.label4)
        hbox[2].addWidget(self.button1)
        hbox[2].addWidget(self.button2)
        hbox[2].addWidget(self.button3)

        vbox.addLayout(hbox[0])
        vbox.addLayout(hbox[1])
        vbox.addWidget(self.label5)
        vbox.addWidget(self.label6)
        vbox.addWidget(self.edit1)
        vbox.addWidget(self.label7)
        vbox.addWidget(self.edit2)
        vbox.addLayout(hbox[2])

        self.setLayout(vbox)

    def reset(self):
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #判定値を0、判定値以外を直近の値として新しくデータを挿入
        a = (seitoidentify,kadaiidentify2,self.code[-1],self.out[-1],self.jikan[-1],self.ruiji[-1],self.err[-1])
        c.execute("insert into seito(seitoname,kadainame,sourcecode,output,compiletime,similarity,error,judgeparameter,tassei) values(?,?,?,?,?,?,?,0,0)", a)
        conn.commit()
        conn.close()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("リセットしました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        m = message.exec_()

        move(5)  #画面更新

    def delete(self):

        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("本当に削除しますか？")
        yesbutton = message.addButton("はい", QMessageBox.ActionRole)
        nobutton = message.addButton("いいえ", QMessageBox.ActionRole)
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("delete from seito where seitoname=?", (seitoidentify,))
            conn.commit()
            conn.close()
            move(2)
        elif message.clickedButton() == nobutton:
            pass

    def quit(self):
        move(2)

    def seitosource(self):
        self.edit1.setPlainText(self.code[-1])  #学習者の入力ソースコードをセット

    def seikaisource(self):
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        self.seikai = []
        c.execute("select seikai from kadai where kadainame=?", (kadaiidentify2,))
        for i in c:
            self.seikai.append(i["seikai"])
        self.edit1.setPlainText(self.seikai[-1])  #正解ソースコードをセット

    def another(self):
        move(6)


class Another(QWidget):
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
        self.button.setGeometry(400,800, 275, 70)
        self.button.clicked.connect(self.quit)

        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        kadaiset = set()

        c.execute("select kadainame from seito where seitoname=?",(seitoidentify,))
        for i in c:
            kadaiset.add(i["kadainame"])  #学習者が今まで開いた課題の配列(被りなし)

        vbox = [QVBoxLayout(),QVBoxLayout(),QVBoxLayout()]
        hbox = QHBoxLayout()
        line = 0
        for name in sorted(kadaiset):
            self.button = QPushButton(name)
            self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
            self.button.setStyleSheet("background-color: Gainsboro")
            self.button.clicked.connect(self.seitodetail)
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

    def seitodetail(self):
        b = self.sender()
        global kadaiidentify2
        kadaiidentify2 = b.text()
        move(5)

    def quit(self):
        move(5)


class App(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("教員用")
        global tab
        tab = Menu(self)
        self.addTab(tab, "Menu")
        
        self.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabBar().hide()
        self.resize(700, 900)
        self.move(300,20)
        self.setStyleSheet('background-color:AliceBlue')


def move(page):

    window.removeTab(0)

    if page == 0:
        tab = Menu(window)
        window.addTab(tab,"Menu")
    elif page == 1:
        tab = KadaiList(window)
        window.addTab(tab,"KadaiList")
    elif page == 2:
        tab = SeitoList(window)
        window.addTab(tab,"SeitoList")
    elif page == 3:
        tab = KadaiHozon(window)
        window.addTab(tab,"KadaiHozon")
    elif page == 4:
        tab = KadaiDetail(window)
        window.addTab(tab,"KadaiDetail")
    elif page == 5:
        tab = SeitoDetail(window)
        window.addTab(tab,"SeitoDetail")
    elif page == 6:
        tab = Another(window)
        window.addTab(tab,"Another")

    window.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    global window
    window = App()
    window.show()
    app.exec_()