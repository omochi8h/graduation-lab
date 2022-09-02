import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *

import sqlite3
import time
import linenumber

method = 1
calc = 1
formula = "(T/300)**2 * 1.5 * (-S+1)**3 * E"


class KadaiList(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.button1 = QPushButton("終了", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.clicked.connect(QCoreApplication.instance().quit)

        self.check1 = QCheckBox('菊岡方式　　　', self)
        self.check1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check1.clicked.connect(self.method1)

        self.check2 = QCheckBox('立花方式　　　', self)
        self.check2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check2.clicked.connect(self.method2)

        self.check3 = QCheckBox('OLD', self)
        self.check3.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check3.clicked.connect(self.calc1)

        self.check4 = QCheckBox('Jaro', self)
        self.check4.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check4.clicked.connect(self.calc2)

        self.check5 = QCheckBox('Dice', self)
        self.check5.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check5.clicked.connect(self.calc3)

        self.check6 = QCheckBox('TED', self)
        self.check6.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check6.clicked.connect(self.calc4)
     
        self.check7 = QCheckBox('TO', self)
        self.check7.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check7.clicked.connect(self.calc5)

        self.label = QLabel("判定値式 ： ", self)
        font = QFont()
        font.setPointSize(17)
        self.label.setFont(font)

        self.edit = QLineEdit(self)
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(20)
        self.edit.setFont(font)
        self.edit.setText(formula)

        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        kadai = set()

        c.execute("select kadainame from jikken")
        for i in c:
            kadai.add(i["kadainame"])

        vbox = [QVBoxLayout(),QVBoxLayout(),QVBoxLayout()]
        hbox = [QHBoxLayout(),QHBoxLayout(),QHBoxLayout(),QHBoxLayout()]
        line = 0
        for name in sorted(kadai):
            self.button = QPushButton(name)
            self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
            self.button.setStyleSheet("background-color: Gainsboro")
            self.button.clicked.connect(self.seitolist)
            vbox[line].addWidget(self.button)
            line += 1
            if line == 3:
                line = 0

        for v in vbox:
            v.addStretch(1)
            hbox[0].addLayout(v)

        hbox[1].addWidget(self.check1)
        hbox[1].addWidget(self.check2)
        hbox[1].addStretch(1)
        hbox[2].addWidget(self.check3)
        hbox[2].addWidget(self.check4)
        hbox[2].addWidget(self.check5)
        hbox[2].addWidget(self.check6)
        hbox[2].addWidget(self.check7)
        hbox[3].addWidget(self.label)
        hbox[3].addWidget(self.edit)

        v = QVBoxLayout()
        v.addLayout(hbox[0])
        v.addLayout(hbox[1])
        v.addLayout(hbox[2])
        v.addLayout(hbox[3])
        v.addWidget(self.button1)
        self.setLayout(v)

        if method == 1:
            self.check1.setChecked(True)
        elif method == 2:
            self.check2.setChecked(True)

        if calc == 1:
            self.check3.setChecked(True)
        elif calc == 2:
            self.check4.setChecked(True)
        elif calc == 3:
            self.check5.setChecked(True)
        elif calc == 4:
            self.check6.setChecked(True)
        elif calc == 5:
            self.check7.setChecked(True)

    def seitolist(self):
        global kadaiidentify
        global method
        global calc
        global formula

        formula = self.edit.text()
        self.button = self.sender()
        kadaiidentify = self.button.text()

        if self.check1.checkState():
            method = 1
        elif self.check2.checkState():
            method = 2

        if self.check3.checkState():
            calc = 1
        elif self.check4.checkState():
            calc = 2
        elif self.check5.checkState():
            calc = 3
        elif self.check6.checkState():
            calc = 4
        elif self.check7.checkState():
            calc = 5

        move(1)

    def method1(self):
        self.check1.setChecked(True)
        self.check2.setChecked(False)

    def method2(self):
        self.check1.setChecked(False)
        self.check2.setChecked(True)

    def calc1(self):
        self.check3.setChecked(True)
        self.check4.setChecked(False)
        self.check5.setChecked(False)
        self.check6.setChecked(False)
        self.check7.setChecked(False)

    def calc2(self):
        self.check3.setChecked(False)
        self.check4.setChecked(True)
        self.check5.setChecked(False)
        self.check6.setChecked(False)
        self.check7.setChecked(False)

    def calc3(self):
        self.check3.setChecked(False)
        self.check4.setChecked(False)
        self.check5.setChecked(True)
        self.check6.setChecked(False)
        self.check7.setChecked(False)

    def calc4(self):
        self.check3.setChecked(False)
        self.check4.setChecked(False)
        self.check5.setChecked(False)
        self.check6.setChecked(True)
        self.check7.setChecked(False)

    def calc5(self):
        self.check3.setChecked(False)
        self.check4.setChecked(False)
        self.check5.setChecked(False)
        self.check6.setChecked(False)
        self.check7.setChecked(True)


class SeitoList(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.button1 = QPushButton("更新", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.clicked.connect(self.upd)

        self.button2 = QPushButton("戻る", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color: Gainsboro")
        self.button2.clicked.connect(self.quit)

        self.label1 = QLabel("課題名 ： " + str(kadaiidentify), self)
        font = QFont()
        font.setPointSize(17)
        self.label1.setFont(font)

        self.label2 = QLabel("判定値式 ： ", self)
        font = QFont()
        font.setPointSize(17)
        self.label2.setFont(font)

        self.edit = QLineEdit(self)
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(20)
        self.edit.setFont(font)
        self.edit.setText(formula)

        self.check1 = QCheckBox('菊岡方式　　　', self)
        self.check1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check1.clicked.connect(self.method1)

        self.check2 = QCheckBox('立花方式　　　', self)
        self.check2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check2.clicked.connect(self.method2)

        self.check3 = QCheckBox('OLD', self)
        self.check3.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check3.clicked.connect(self.calc1)

        self.check4 = QCheckBox('Jaro', self)
        self.check4.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check4.clicked.connect(self.calc2)

        self.check5 = QCheckBox('Dice', self)
        self.check5.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check5.clicked.connect(self.calc3)

        self.check6 = QCheckBox('TED', self)
        self.check6.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check6.clicked.connect(self.calc4)
     
        self.check7 = QCheckBox('TO', self)
        self.check7.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.check7.clicked.connect(self.calc5)


        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        seitoset = set()

        c.execute("select seitoname from jikken where kadainame=?",(kadaiidentify,))
        for i in c:
            seitoset.add(i["seitoname"])
            
        vbox = [QVBoxLayout(),QVBoxLayout(),QVBoxLayout()]
        hbox = [QHBoxLayout(),QHBoxLayout(),QHBoxLayout(),QHBoxLayout(),QHBoxLayout()]
        line = 0

        if method == 1:
            for seito in sorted(seitoset):
                jikan = []
                old = []
                jaro = []
                dice = []
                ted = []
                to = []
                err = []

                c.execute("select*from jikken where seitoname=? and kadainame=?", (seito,kadaiidentify))
                for i in c:
                    jikan.append(i["compiletime"])
                    old.append(i["simiold"])
                    jaro.append(i["simijaro"])
                    dice.append(i["simidice"])
                    ted.append(i["simited"])
                    to.append(i["simito"])
                    err.append(i["error"])

                judge = 0
                name = seito + "\n"

                if calc == 1:
                    name = name + "類似度：" + str(old[-1])
                elif calc == 2:
                    name = name + "類似度：" + str(jaro[-1])
                elif calc == 3:
                    name = name + "類似度：" + str(dice[-1])
                elif calc == 4:
                    name = name + "類似度：" + str(ted[-1])
                elif calc == 5:
                    name = name + "類似度：" + str(to[-1])

                for i in range(len(jikan)):
                    if i == 0:
                        pass
                    else:
                        T = jikan[i] - jikan[i-1]
                        if calc == 1:
                            S = old[i] - old[i-1]
                        elif calc == 2:
                            S = jaro[i] - jaro[i-1]
                        elif calc == 3:
                            S = dice[i] - dice[i-1]
                        elif calc == 4:
                            S = ted[i] - ted[i-1]
                        elif calc == 5:
                            S = to[i] - to[i-1]
                        E = err[i]
                        judge = judge + eval(self.edit.text())
                        #print("コンパイル間隔：" + str(T))
                        #print("類似度：" + str(S))
                        #print("エラー倍率：" + str(E))
                        #print(eval(self.edit.text()))
                        #print("\n")

                name = name + "\n判定値：" + str(round(judge, 3))
                self.button = QPushButton(name)
                self.button.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))

                if judge >= 3:
                    self.button.setStyleSheet("background-color: red")
                else:
                    self.button.setStyleSheet("background-color: Gainsboro")

                self.button.index = seito
                self.button.clicked.connect(self.seitodetail)
                vbox[line].addWidget(self.button)
                line += 1
                if line == 3:
                    line = 0

        elif method == 2:
            for seito in sorted(seitoset):
                old = []
                jaro = []
                dice = []
                ted = []
                to = []
                err = []

                c.execute("select*from jikken where seitoname=? and kadainame=?", (seito,kadaiidentify))
                for i in c:
                    old.append(i["simiold"])
                    jaro.append(i["simijaro"])
                    dice.append(i["simidice"])
                    ted.append(i["simited"])
                    to.append(i["simito"])
                    err.append(i["error"])

                name = seito + "\n"

                if calc == 1:
                    name = name + "類似度：" + str(old[-1])
                elif calc == 2:
                    name = name + "類似度：" + str(jaro[-1])
                elif calc == 3:
                    name = name + "類似度：" + str(dice[-1])
                elif calc == 4:
                    name = name + "類似度：" + str(ted[-1])
                elif calc == 5:
                    name = name + "類似度：" + str(to[-1])

                judge = 0
                for i in range(len(old)):
                    if i == 0:
                        pass
                    else:
                        if calc == 1:
                            S = old[i] - old[i-1]
                        elif calc == 2:
                            S = jaro[i] - jaro[i-1]
                        elif calc == 3:
                            S = dice[i] - dice[i-1]
                        elif calc == 4:
                            S = ted[i] - ted[i-1]
                        elif calc == 5:
                            S = to[i] - to[i-1]

                        if err[i] == 0.5:
                            judge = 0
                        else:
                            if S >= 0:
                                judge = judge + 1
                            else:
                                if judge < 3:
                                    judge = 0

                self.button = QPushButton(name)
                self.button.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))

                if judge >= 3:
                    self.button.setStyleSheet("background-color: red")
                else:
                    self.button.setStyleSheet("background-color: Gainsboro")

                self.button.index = seito
                self.button.clicked.connect(self.seitodetail)
                vbox[line].addWidget(self.button)
                line += 1
                if line == 3:
                    line = 0
            

        for v in vbox:
            v.addStretch(1)
            hbox[0].addLayout(v)

        hbox[1].addWidget(self.check1)
        hbox[1].addWidget(self.check2)
        hbox[1].addStretch(1)
        hbox[2].addWidget(self.check3)
        hbox[2].addWidget(self.check4)
        hbox[2].addWidget(self.check5)
        hbox[2].addWidget(self.check6)
        hbox[2].addWidget(self.check7)
        hbox[3].addWidget(self.label2)
        hbox[3].addWidget(self.edit)
        hbox[4].addWidget(self.button1)
        hbox[4].addWidget(self.button2)

        v = QVBoxLayout()
        v.addWidget(self.label1)
        v.addLayout(hbox[0])
        v.addLayout(hbox[1])
        v.addLayout(hbox[2])
        v.addLayout(hbox[3])
        v.addLayout(hbox[4])

        self.setLayout(v)

        if method == 1:
            self.check1.setChecked(True)
        elif method == 2:
            self.check2.setChecked(True)

        if calc == 1:
            self.check3.setChecked(True)
        elif calc == 2:
            self.check4.setChecked(True)
        elif calc == 3:
            self.check5.setChecked(True)
        elif calc == 4:
            self.check6.setChecked(True)
        elif calc == 5:
            self.check7.setChecked(True)


    def method1(self):
        self.check1.setChecked(True)
        self.check2.setChecked(False)

    def method2(self):
        self.check1.setChecked(False)
        self.check2.setChecked(True)

    def calc1(self):
        self.check3.setChecked(True)
        self.check4.setChecked(False)
        self.check5.setChecked(False)
        self.check6.setChecked(False)
        self.check7.setChecked(False)

    def calc2(self):
        self.check3.setChecked(False)
        self.check4.setChecked(True)
        self.check5.setChecked(False)
        self.check6.setChecked(False)
        self.check7.setChecked(False)

    def calc3(self):
        self.check3.setChecked(False)
        self.check4.setChecked(False)
        self.check5.setChecked(True)
        self.check6.setChecked(False)
        self.check7.setChecked(False)

    def calc4(self):
        self.check3.setChecked(False)
        self.check4.setChecked(False)
        self.check5.setChecked(False)
        self.check6.setChecked(True)
        self.check7.setChecked(False)

    def calc5(self):
        self.check3.setChecked(False)
        self.check4.setChecked(False)
        self.check5.setChecked(False)
        self.check6.setChecked(False)
        self.check7.setChecked(True)

    def seitodetail(self):
        global seitoidentify
        self.button = self.sender()
        seitoidentify = self.button.index

        global formula
        formula = self.edit.text()

        move(2)

    def upd(self):
        global method
        global calc
        if self.check1.checkState():
            method = 1
        elif self.check2.checkState():
            method = 2

        if self.check3.checkState():
            calc = 1
        elif self.check4.checkState():
            calc = 2
        elif self.check5.checkState():
            calc = 3
        elif self.check6.checkState():
            calc = 4
        elif self.check7.checkState():
            calc = 5

        global formula
        formula = self.edit.text()

        move(1)

    def quit(self):
        global method
        global calc
        if self.check1.checkState():
            method = 1
        elif self.check2.checkState():
            method = 2

        if self.check3.checkState():
            calc = 1
        elif self.check4.checkState():
            calc = 2
        elif self.check5.checkState():
            calc = 3
        elif self.check6.checkState():
            calc = 4
        elif self.check7.checkState():
            calc = 5

        global formula
        formula = self.edit.text()

        move(0)


class SeitoDetail(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        code = []
        out = []
        jikan = []
        old = []
        jaro = []
        dice = []
        ted = []
        to = []
        err = []

        c.execute("select*from jikken where seitoname=? and kadainame=?", (seitoidentify,kadaiidentify))
        for i in c:
            code.append(i["sourcecode"])
            out.append(i["output"])
            jikan.append(i["compiletime"])
            old.append(i["simiold"])
            jaro.append(i["simijaro"])
            dice.append(i["simidice"])
            ted.append(i["simited"])
            to.append(i["simito"])
            err.append(i["error"])

        self.label1 = QLabel("学習者名 ： " + str(seitoidentify), self)
        font = QFont()
        font.setPointSize(13)
        self.label1.setFont(font)

        self.label2 = QLabel("課題名 ： " + str(kadaiidentify), self)
        font = QFont()
        font.setPointSize(13)
        self.label2.setFont(font)

        self.label3 = QLabel("類似度", self)
        font = QFont()
        font.setPointSize(13)
        self.label3.setFont(font)

        self.label4 = QLabel("判定値", self)
        font = QFont()
        font.setPointSize(13)
        self.label4.setFont(font)

        self.label8 = QLabel("判定値式 ： ", self)
        font = QFont()
        font.setPointSize(13)
        self.label8.setFont(font)

        self.edit4 = QLineEdit(self)
        self.edit4.setStyleSheet('background-color: white')
        font = self.edit4.font()
        font.setPointSize(16)
        self.edit4.setFont(font)
        self.edit4.setText(formula)

        name = "コンパイル時間 ： "
        for i in range(len(jikan)):
            if i == 0:
                pass
            else:
                name = name + str(round((time.time()-jikan[i])/60)) + "分前，"
        name = name.rstrip("，")
        self.label5 = QLabel(name, self)
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

        self.edit3 = QTextEdit(self)
        self.edit3.setStyleSheet('background-color: white')
        font = self.edit3.font()  
        font.setPointSize(13)
        self.edit3.setFont(font)
        
        self.button1 = QPushButton("学習者削除", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color: Gainsboro")
        self.button1.clicked.connect(self.delete)

        self.button2 = QPushButton("戻る", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color: Gainsboro")
        self.button2.clicked.connect(self.quit)

        self.button3 = QPushButton("学習者", self)
        self.button3.setFont(QtGui.QFont("MS　ゴシック", 13, QFont.Medium))
        self.button3.setStyleSheet("background-color: Gainsboro")
        self.button3.clicked.connect(self.seitosource)

        self.button4 = QPushButton("正解", self)
        self.button4.setFont(QtGui.QFont("MS　ゴシック", 13, QFont.Medium))
        self.button4.setStyleSheet("background-color: Gainsboro")
        self.button4.clicked.connect(self.seikaisource)

        self.source = ""
        for i in range(len(code)):
            if i == 0:
                pass
            else:
                self.source = self.source + "＜" + str(i) + "回目＞\n" + code[i] + "\n\n\n"
        self.edit1.setPlainText(self.source)

        text = ""
        for i in range(len(out)):
            if i == 0:
                pass
            else:
                text = text + "＜" + str(i) + "回目＞\n" + out[i] + "\n\n\n"
        self.edit2.setPlainText(text)

        text = ""
        judge = [0,0,0,0,0]
        for i in range(len(old)):
            if i == 0:
                pass
            else:
                for j in range(5):
                    T = jikan[i] - jikan[i-1]
                    if j == 0:
                        S = old[i] - old[i-1]
                    elif j == 1:
                        S = jaro[i] - jaro[i-1]
                    elif j == 2:
                        S = dice[i] - dice[i-1]
                    elif j == 3:
                        S = ted[i] - ted[i-1]
                    elif j == 4:
                        S = to[i] - to[i-1]
                    E = err[i]
                    judge[j] = judge[j] + eval(self.edit4.text())

                text = text + "＜" + str(i) + "回目＞　　　　　　　　　　　　　　　　　　　　　＜" + str(i) + "回目＞\n"
                text = text + "OLD      Jaro      Dice      TED      TO         OLD      Jaro      Dice      TED      TO\n"
                text = text + str(old[i]) + " "*(9-len(str(old[i]))) + str(jaro[i]) + " "*(10-len(str(jaro[i]))) + str(dice[i]) + " "*(10-len(str(dice[i]))) + str(ted[i]) + " "*(10-len(str(ted[i]))) + str(to[i]) + " "*(10-len(str(to[i])))
                text = text + str(round(judge[0], 3)) + " "*(9-len(str(round(judge[0],3)))) + str(round(judge[1], 3)) + " "*(9-len(str(round(judge[1],3)))) + str(round(judge[2], 3)) + " "*(9-len(str(round(judge[2],3)))) + str(round(judge[3], 3)) + " "*(9-len(str(round(judge[3],3)))) + str(round(judge[4], 3)) + "\n\n\n"
        self.edit3.setPlainText(text)

        hbox = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(),QHBoxLayout()]
        vbox = QVBoxLayout()

        hbox[0].addWidget(self.label1)
        hbox[0].addWidget(self.label2)
        hbox[1].addWidget(self.label8)
        hbox[1].addWidget(self.edit4)
        hbox[2].addWidget(self.label3)
        hbox[2].addWidget(self.label4)
        hbox[3].addWidget(self.label6)
        hbox[3].addWidget(self.button3)
        hbox[3].addWidget(self.button4)
        hbox[4].addLayout(hbox[3])
        hbox[4].addWidget(self.label7)
        hbox[5].addWidget(self.edit1)
        hbox[5].addWidget(self.edit2)
        hbox[6].addWidget(self.button1)
        hbox[6].addWidget(self.button2)

        vbox.addLayout(hbox[0])
        vbox.addWidget(self.label5)
        vbox.addLayout(hbox[1])
        vbox.addLayout(hbox[2])
        vbox.addWidget(self.edit3)
        vbox.addLayout(hbox[4])
        vbox.addLayout(hbox[5])
        vbox.addLayout(hbox[6])

        self.setLayout(vbox)

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
            c.execute("delete from jikken where seitoname=?", (seitoidentify,))
            conn.commit()
            conn.close()
            move(1)
        elif message.clickedButton() == nobutton:
            pass

    def quit(self):
        move(1)

    def seitosource(self):
        self.edit1.setPlainText(self.source)  #学習者の入力ソースコードをセット

    def seikaisource(self):
        conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        self.seikai = []
        c.execute("select seikai from kadai where kadainame=?", (kadaiidentify,))
        for i in c:
            self.seikai.append(i["seikai"])
        self.edit1.setPlainText(self.seikai[-1])  #正解ソースコードをセット


class App(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("実験用")
        global tab
        tab = KadaiList(self)
        self.addTab(tab, "KadaiList")
        
        self.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabBar().hide()
        self.resize(700, 900)
        self.move(300,20)
        self.setStyleSheet('background-color:AliceBlue')


def move(page):

    window.removeTab(0)

    if page == 0:
        tab = KadaiList(window)
        window.addTab(tab,"KadaiList")
    elif page == 1:
        tab = SeitoList(window)
        window.addTab(tab,"SeitoList")
    elif page == 2:
        tab = SeitoDetail(window)
        window.addTab(tab,"SeitoDetail")

    window.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    global window
    window = App()
    window.show()
    app.exec_()