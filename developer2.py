
import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import *

import sqlite3
import time
import linenumber

kadaiidentify = 0
seitoidentify = ""
narabi = 0
mushi = "1"
mush = 0
method = "OLD"

conn = sqlite3.connect('C:\\Users\\student\\OneDrive\\data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        hbox = QHBoxLayout()

        global menu
        menu = Menu(self)
        menu.setFrameShape(QFrame.Panel)

        global manual
        manual = Manual(self)
        manual.setFrameShape(QFrame.Panel)

        global kadaihozon
        kadaihozon = KadaiHozon(self)
        kadaihozon.setFrameShape(QFrame.Panel)

        global kadaidetail
        kadaidetail = KadaiDetail(self)
        kadaidetail.setFrameShape(QFrame.Panel)

        global seitodetail
        seitodetail = SeitoDetail(self)
        seitodetail.setFrameShape(QFrame.Panel)

        hbox.addWidget(menu)
        hbox.addWidget(manual)
        hbox.addWidget(kadaihozon)
        hbox.addWidget(kadaidetail)
        hbox.addWidget(seitodetail)

        kadaihozon.hide()
        kadaidetail.hide()
        seitodetail.hide()

        self.setLayout(hbox)


class Menu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        button1 = QPushButton("更新", self)
        button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        button1.setStyleSheet("background-color:Gainsboro")
        button1.clicked.connect(self.renew)

        button2 = QPushButton("新規課題保存", self)
        button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        button2.setStyleSheet("background-color:Gainsboro")
        button2.clicked.connect(self.kadaihozon)

        button3 = QPushButton("終了", self)
        button3.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        button3.setStyleSheet("background-color:Gainsboro")
        button3.clicked.connect(self.syuuryou)

        simimethod = ["OLD","Jaro","DC","TED","TO"]
        h4 = QHBoxLayout()
        for i in simimethod:
            radio = QRadioButton("{}".format(i))
            radio.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
            if method == i:
                radio.setChecked(True)
            radio.toggled.connect(self.click)
            h4.addWidget(radio)
        

        label1 = QLabel('課題を選択してください')
        font = QFont()
        font.setPointSize(17)
        label1.setFont(font)

        label2 = QLabel('学習者リスト')
        font = QFont()
        font.setPointSize(17)
        label2.setFont(font)

        self.edit = QLineEdit(self)
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(20)
        self.edit.setFont(font)
        self.edit.setTextMargins(0,0,0,0)
        self.edit.setAlignment(Qt.AlignCenter)
        self.edit.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Minimum)
        self.edit.setText(mushi)

        self.check = QCheckBox(" ")
        if mush == 1:
            self.check.setChecked(True)
        self.check.clicked.connect(self.ignore)

        label3 = QLabel('日以上前のデータを無視')
        font = QFont()
        font.setPointSize(17)
        label3.setFont(font)

        label4 = QLabel(' ')
        font = QFont()
        font.setPointSize(17)
        label4.setFont(font)

        space = QSpacerItem(100,40,QSizePolicy.Maximum,QSizePolicy.Maximum)

        self.combobox1 = QComboBox()
        font = QFont()
        font.setPointSize(17)
        self.combobox1.setFont(font)
        self.combobox1.setStyleSheet("background-color:white")
        kadailist = ["取り組み中の課題"]
        c.execute("select kadainame from kadai")
        for kadai in c:
            kadailist.append(kadai["kadainame"])
        self.combobox1.addItems(kadailist)
        self.combobox1.setCurrentIndex(kadaiidentify)
        self.combobox1.currentIndexChanged.connect(self.kadaisentaku)

        self.combobox2 = QComboBox()
        font = QFont()
        font.setPointSize(17)
        self.combobox2.setFont(font)
        self.combobox2.setStyleSheet("background-color:white")
        sortlist = ["名前順","課題名順","最後のコンパイルが古い順","判定値が大きい順"]
        self.combobox2.addItems(sortlist)
        self.combobox2.setCurrentIndex(narabi)
        self.combobox2.currentIndexChanged.connect(self.narabikae)

        table = ScrollTable(self)
        h1 = QHBoxLayout()
        v1 = QVBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        h2.addWidget(label4)
        h2.addWidget(label4)
        h2.addWidget(label4)
        for i in range(3):
            h3.addWidget(label4)
        h3.addWidget(self.check)
        h2.addLayout(h3)
        h2.addWidget(self.edit)
        h2.addWidget(label3)
        h1.addWidget(button1)
        h1.addWidget(button2)
        h1.addWidget(button3)
        v1.addSpacerItem(space)
        v1.addWidget(label1)
        v1.addWidget(self.combobox1)
        v1.addSpacerItem(space)
        v1.addWidget(label2)
        v1.addWidget(self.combobox2)
        v1.addLayout(h2)
        v1.addWidget(table)
        v1.addSpacerItem(space)
        v1.addLayout(h4)
        v1.addLayout(h1)
        self.setLayout(v1)


    def renew(self):
        global mush
        global mushi
        if self.check.checkState():
            try:
                float(self.edit.text())
            except:
                message = QMessageBox()
                message.setWindowTitle("失敗")
                message.setText("数字のみで入力してください")
                okbutton = message.addButton("OK", QMessageBox.AcceptRole)
                message.setDefaultButton(okbutton)
                m = message.exec_()
                move(0)
            else:
                mushi = self.edit.text()
                mush = 1
                move(0)
        else:
            mush = 0
            mushi = self.edit.text()
            move(0)

    def kadaihozon(self):
        move(1)

    def click(self):
        r = self.sender()
        global method
        method = r.text()
        move(3)

    def kadaisentaku(self):
        global kadaiidentify
        kadaiidentify = self.combobox1.currentIndex()
        if kadaiidentify == 0:
            move(0)
        else:
            move(2)

    def narabikae(self):
        global narabi
        narabi = self.combobox2.currentIndex()
        move(0)

    def ignore(self):
        self.renew()

    def syuuryou(self):
        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("終了しますか？")
        yesbutton = message.addButton("はい", QMessageBox.ActionRole)
        nobutton = message.addButton("いいえ", QMessageBox.ActionRole)
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            QCoreApplication.instance().quit()
        elif message.clickedButton() == nobutton:
            pass
        

class ScrollTable(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        vbox = QVBoxLayout()
        seitoset = set()
        data = []
        c.execute("select seitoname from seito")
        for i in c:
            seitoset.add(i["seitoname"])
        for seito in sorted(seitoset):
            row = []
            kadai = []
            jikan = []
            ruijiold = [0]
            ruijijaro = [0]
            ruijidc = [0]
            ruijited = [0]
            ruijito = [0]
            err = [1]
            achieve = [0]
            comp = []
            kadailist = ["No Data"]
            c.execute("select kadainame from seito where seitoname=? and comp=1", (seito,))
            for i in c:
                kadailist.append(i["kadainame"])
            kadai.append(kadailist[-1])
            c.execute("select kadainame from kadai")
            for i in c:
                kadai.append(i["kadainame"])
            c.execute("select*from seito where seitoname=? and kadainame=? and comp=1", (seito,kadai[kadaiidentify]))
            for i in c:
                ruijiold.append(i["simiold"])
                ruijijaro.append(i["simijaro"])
                ruijidc.append(i["simidc"])
                ruijited.append(i["simited"])
                ruijito.append(i["simito"])
                err.append(i["error"])
                achieve.append(i["tassei"])
            c.execute("select*from seito where seitoname=? and kadainame=?", (seito,kadai[kadaiidentify]))
            for i in c:
                jikan.append(i["compiletime"])
                comp.append(i["comp"])
            jikansuii = [0]
            for i in range(len(comp)):
                if comp[i] == 1:
                    suii = jikan[i] - jikan[i-1]
                    jikansuii.append(suii)

            if method == "OLD":
                ruiji = ruijiold
            elif method == "Jaro":
                ruiji = ruijijaro
            elif method == "DC":
                ruiji = ruijidc
            elif method == "TED":
                ruiji = ruijited
            elif method == "TO":
                ruiji = ruijito
            judge = 0
            for i in range(1,len(ruiji)):
                S = ruiji[i] - ruiji[i-1]
                E = err[i]
                T = jikansuii[i]
                judge = judge + (T/300)**2 * 1.5 * (-S+1)**3 * E

            row.append(seito)
            row.append(kadai[kadaiidentify])
            try:
                row.append(round((time.time()-jikan[-1])/60))  #コンパイル以外も含まれてしまう
            except:
                row.append(100000000)
            row.append(round(judge,3))
            row.append(achieve[-1])
            if 100000000 != row[2]:
                data.append(row)
        
        self.table = QTableWidget(len(data),6)
        self.table.setStyleSheet("background-color: White")
        self.table.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)
        self.table.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = ["学習者名","課題名","コンパイル時間","判定値","達成状況",""]
        self.table.setHorizontalHeaderLabels(header)
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5,QHeaderView.ResizeToContents)
        if narabi == 1:
            data = sorted(data,key=lambda x:x[1])
        elif narabi == 2:
            data = sorted(data,key=lambda x:x[2],reverse=True)
        elif narabi == 3:
            data = sorted(data,key=lambda x:x[3],reverse=True)

        if mush == 1:
            data = [i for i in data if i[2]<=float(mushi)*1440]
        for d in data:
            d[0] = " " + str(d[0]) + " "
            d[1] = " " + str(d[1]) + " "
            d[2] = " " + str(d[2]) + "分前 "
            d[3] = " " + str(d[3]) + " "
            if d[4] == 0:
                d[4] = "未"
            else:
                d[4] = " 達成 "

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.table.setItem(i,j,QTableWidgetItem(data[i][j]))
            if float(data[i][3]) >= 4:
                self.table.item(i,3).setBackground(QColor(255,80,80))
            if "未" in data[i][4]:
                self.table.item(i,4).setForeground(QColor(0,0,150))
            else:
                self.table.item(i,4).setForeground(QColor(255,0,0))
            for j in range(len(data[i])):
                self.table.item(i,j).setTextAlignment(Qt.AlignCenter)

            button = QPushButton("詳細")
            button.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))
            button.setStyleSheet("background-color:whitesmoke")
            button.index = data[i][0].replace(" ","")
            button.clicked.connect(self.seitodetail)
            if seitoidentify == button.index:
                button.setStyleSheet("background-color:khaki")
            self.table.setCellWidget(i,5,button)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def seitodetail(self):
        global seitoidentify
        s = self.sender()
        seitoidentify = s.index
        move(3)


class Manual(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label1 = QLabel("課題を選ぶと詳細が表示されます。\n課題の編集・削除が可能です。")
        font = QFont()
        font.setPointSize(15)
        self.label1.setFont(font)

        self.label2 = QLabel("学習者リストを指定の方法で並び変えることができます。\n\nテキストボックスに実数を入れてチェックを入れると\n指定した日数以前のデータが表示されなくなります。")
        font = QFont()
        font.setPointSize(15)
        self.label2.setFont(font)

        self.label3 = QLabel("判定値：高いほど躓いている可能性が高いです。\n　　　　　 判定値が4以上のものはセルが赤くなります。")
        font = QFont()
        font.setPointSize(15)
        self.label3.setFont(font)

        self.label4 = QLabel("更新：画面を更新\n新規課題保存：新しい課題をデータベースに保存\n終了：アプリを終了")
        font = QFont()
        font.setPointSize(15)
        self.label4.setFont(font)

        v = QVBoxLayout()
        space = QSpacerItem(100,60,QSizePolicy.Maximum,QSizePolicy.Maximum)
        v.addSpacerItem(space)
        v.addWidget(self.label1)
        v.addSpacerItem(space)
        v.addWidget(self.label2)
        v.addStretch(1)
        v.addWidget(self.label3)
        v.addStretch(1)
        v.addWidget(self.label4)
        self.setLayout(v)


class KadaiHozon(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QPushButton("保存", self)
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color:Gainsboro")
        self.button.clicked.connect(self.save)

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
        self.edit1.setStyleSheet('background-color:white')
        font = self.edit1.font()  
        font.setPointSize(13)
        self.edit1.setFont(font)

        self.edit2 = QTextEdit(self)
        self.edit2.setStyleSheet('background-color:white')
        font = self.edit2.font()  
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.edit3 = QTextEdit(self)
        self.edit3.setStyleSheet('background-color:white')
        font = self.edit3.font()  
        font.setPointSize(13)
        self.edit3.setFont(font)

        grid = QGridLayout()

        grid.addWidget(self.label1,0,0,1,2)
        grid.addWidget(self.edit1,1,0,1,2)
        grid.addWidget(self.label2,2,0,1,2)
        grid.addWidget(self.edit2,3,0,1,2)
        grid.addWidget(self.label3,4,0,1,2)
        grid.addWidget(self.edit3,5,0,1,2)
        grid.addWidget(self.button,6,0,1,2)
        self.setLayout(grid)

    def save(self):
        self.Text1 = self.edit1.text()
        self.Text2 = self.edit2.toPlainText()
        self.Text3 = self.edit3.toPlainText()
        a = (self.Text1, self.Text2, self.Text3)

        c.execute("insert into kadai(kadainame,mondaibun,seikai) values(?,?,?)", a)
        conn.commit()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("保存しました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setDetailedText(self.Text1 + '\n\n' + self.Text2 + '\n\n' + self.Text3)
        m = message.exec_()
        move(0)


class KadaiDetail(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button1 = QPushButton("編集", self)
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color:Gainsboro")
        self.button1.clicked.connect(self.save)

        self.button2 = QPushButton("課題削除", self)
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color:Gainsboro")
        self.button2.clicked.connect(self.delete)

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

        grid.addWidget(self.label1, 0, 0, 1, 2)
        grid.addWidget(self.edit1, 1, 0, 1, 2)
        grid.addWidget(self.label2, 2, 0, 1, 2)
        grid.addWidget(self.edit2, 3, 0, 1, 2)
        grid.addWidget(self.label3, 4, 0, 1, 2)
        grid.addWidget(self.edit3, 5, 0, 1, 2)
        grid.addWidget(self.button1, 6, 0, 1, 1)
        grid.addWidget(self.button2, 6, 1, 1, 1)
        self.setLayout(grid)

        list1=["課題名",]
        list2=["問題文",]
        list3=["正解",]

        c.execute("select*from kadai")
        for i in c:
            list1.append((i["kadainame"]))
            list2.append((i["mondaibun"]))
            list3.append((i["seikai"]))

        self.text1 = list1[kadaiidentify]
        self.text2 = list2[kadaiidentify]
        self.text3 = list3[kadaiidentify]

        self.edit1.setText(self.text1)
        self.edit2.setPlainText(self.text2)
        self.edit3.setPlainText(self.text3)
        

    def save(self):
        self.Text1 = self.edit1.text()
        self.Text2 = self.edit2.toPlainText()
        self.Text3 = self.edit3.toPlainText()
        a = (self.Text1, self.Text2, self.Text3, self.text1)

        c.execute("update kadai set kadainame=?,mondaibun=?,seikai=? where kadainame=?", a)
        conn.commit()

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
            c.execute("delete from kadai where kadainame=?", (self.text1,))
            c.execute("delete from seito where kadainame=?", (self.text1,))
            conn.commit()
            global kadaiidentify
            kadaiidentify = 0
            move(0)
        elif message.clickedButton() == nobutton:
            pass


class ScrollTable2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        vbox = QVBoxLayout()
        data = []
        kadai = []
        jikan = []
        ruijiold = [0]
        ruijijaro = [0]
        ruijidc = [0]
        ruijited = [0]
        ruijito = [0]
        err = [1]
        achieve = [0]
        comp = []
        kadailist = ["No Data"]
        c.execute("select kadainame from seito where seitoname=? and comp=1", (seitoidentify,))
        for i in c:
            kadailist.append(i["kadainame"])
        kadai.append(kadailist[-1])
        c.execute("select kadainame from kadai")
        for i in c:
            kadai.append(i["kadainame"])
        c.execute("select*from seito where seitoname=? and kadainame=? and comp=1", (seitoidentify,kadai[kadaiidentify]))
        for i in c:
            ruijiold.append(i["simiold"])
            ruijijaro.append(i["simijaro"])
            ruijidc.append(i["simidc"])
            ruijited.append(i["simited"])
            ruijito.append(i["simito"])
            err.append(i["error"])
            achieve.append(i["tassei"])
        c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadai[kadaiidentify]))
        for i in c:
            jikan.append(i["compiletime"])
            comp.append(i["comp"])
        jikansuii = [0]
        for i in range(len(comp)):
            if comp[i] == 1:
                suii = jikan[i] - jikan[i-1]
                jikansuii.append(suii)
        simimethod = [ruijiold,ruijijaro,ruijidc,ruijited,ruijito]
        judges = [0,0,0,0,0]
        for i in range(1,len(ruijiold)):
            row = []
            for simi in simimethod:
                row.append(simi[i])
            for j in range(5):
                S = simimethod[j][i] - simimethod[j][i-1]
                E = err[i]
                T = jikansuii[i]
                judges[j] = judges[j] + (T/300)**2 * 1.5 * (-S+1)**3 * E
                row.append(round(judges[j],3))
            data.append(row)
        
        self.table = QTableWidget(len(data),10)
        self.table.setStyleSheet("background-color: White")
        self.table.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)
        self.table.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = ["S(OLD)","S(Jaro)","S(DC)","S(TED)","S(TO)","J(OLD)","J(Jaro)","J(DC)","J(TED)","J(TO)"]
        self.table.setHorizontalHeaderLabels(header)
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(8,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(9,QHeaderView.ResizeToContents)

        for d in data:
            d[0] = " " + str(d[0]) + " "
            d[1] = " " + str(d[1]) + " "
            d[2] = " " + str(d[2]) + " "
            d[3] = " " + str(d[3]) + " "
            d[4] = " " + str(d[4]) + " "
            d[5] = " " + str(d[5]) + " "
            d[6] = " " + str(d[6]) + " "
            d[7] = " " + str(d[7]) + " "
            d[8] = " " + str(d[8]) + " "
            d[9] = " " + str(d[9]) + " "

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.table.setItem(i,j,QTableWidgetItem(data[i][j]))
            for k in range(5,10):
                if float(data[i][k]) >= 4:
                    self.table.item(i,k).setBackground(QColor(255,80,80))
            for j in range(len(data[i])):
                self.table.item(i,j).setTextAlignment(Qt.AlignCenter)
        vbox.addWidget(self.table)
        self.setLayout(vbox)


class SeitoDetail(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        if seitoidentify != "":
            self.code = []
            out = []
            jikan = []
            kadai = []
            self.kadai = []
            c.execute("select*from seito where seitoname=?", (seitoidentify,))
            for i in c:
                kadai.append(i["kadainame"])
            self.kadai.append(kadai[-1])
            c.execute("select kadainame from kadai")
            for i in c:
                self.kadai.append(i["kadainame"])
            c.execute("select*from seito where seitoname=? and kadainame=? and comp=1", (seitoidentify,self.kadai[kadaiidentify]))
            for i in c:
                self.code.append(i["sourcecode"])
                out.append(i["output"])
                jikan.append(i["compiletime"])

            label1 = QLabel("学習者名 ： " + str(seitoidentify))
            font = QFont()
            font.setPointSize(13)
            label1.setFont(font)

            label2 = QLabel("課題名 ： " + self.kadai[kadaiidentify])
            font = QFont()
            font.setPointSize(13)
            label2.setFont(font)

            label3 = QLabel("類似度")
            font = QFont()
            font.setPointSize(13)
            label3.setFont(font)

            label4 = QLabel("判定値")
            font = QFont()
            font.setPointSize(13)
            label4.setFont(font)

            label5 = QLabel("最後のコンパイル時間 ： " + str(round((time.time()-jikan[-1])/60)) + "分前")
            font = QFont()
            font.setPointSize(13)
            label5.setFont(font)

            label6 = QLabel("ソースコード")
            font = QFont()
            font.setPointSize(13)
            label6.setFont(font)

            label7 = QLabel("出力")
            font = QFont()
            font.setPointSize(13)
            label7.setFont(font)

            self.edit1 = linenumber.QCodeEditor()
            self.edit1.setStyleSheet('background-color: white')
            font = self.edit1.font()  
            font.setPointSize(13)
            self.edit1.setFont(font)

            edit2 = QTextEdit()
            edit2.setStyleSheet('background-color: white')
            font = edit2.font()  
            font.setPointSize(13)
            edit2.setFont(font)

            button1 = QPushButton("判定値リセット")
            button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
            button1.setStyleSheet("background-color: Gainsboro")
            button1.clicked.connect(self.reset)
        
            button2 = QPushButton("学習者削除")
            button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
            button2.setStyleSheet("background-color: Gainsboro")
            button2.clicked.connect(self.delete)

            button3 = QPushButton("学習者")
            button3.setFont(QtGui.QFont("MS　ゴシック", 13, QFont.Medium))
            button3.setStyleSheet("background-color: Gainsboro")
            button3.clicked.connect(self.seitosource)

            button4 = QPushButton("正解")
            button4.setFont(QtGui.QFont("MS　ゴシック", 13, QFont.Medium))
            button4.setStyleSheet("background-color: Gainsboro")
            button4.clicked.connect(self.seikaisource)

            self.edit1.setPlainText(self.code[-1])
            edit2.setPlainText(out[-1])

            table = ScrollTable2(self)
            grid = QGridLayout()
            grid.addWidget(label1,0,0,1,3)
            grid.addWidget(label2,0,3,1,3)
            grid.addWidget(label5,1,0,1,6)
            grid.addWidget(label3,2,0,1,3)
            grid.addWidget(label4,2,3,1,3)
            grid.addWidget(table,3,0,1,6)
            grid.addWidget(label6,4,0,1,6)
            grid.addWidget(button3,4,4,1,1)
            grid.addWidget(button4,4,5,1,1)
            grid.addWidget(self.edit1,5,0,1,6)
            grid.addWidget(label7,6,0,1,6)
            grid.addWidget(edit2,7,0,1,6)
            grid.addWidget(button1,8,0,1,3)
            grid.addWidget(button2,8,3,1,3)
            self.setLayout(grid)

    def reset(self):
        a = (seitoidentify,self.kadai[kadaiidentify])
        c.execute("update seito set judgeparameter=0 where seitoname=? and kadainame=?", a)
        conn.commit()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("リセットしました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        m = message.exec_()

        move(3)

    def delete(self):

        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("本当に削除しますか？")
        yesbutton = message.addButton("はい", QMessageBox.ActionRole)
        nobutton = message.addButton("いいえ", QMessageBox.ActionRole)
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            c.execute("delete from seito where seitoname=?", (seitoidentify,))
            conn.commit()
            move(0)
        elif message.clickedButton() == nobutton:
            pass

    def seitosource(self):
        self.edit1.setPlainText(self.code[-1])  #学習者の入力ソースコードをセット

    def seikaisource(self):
        seikai = []
        c.execute("select seikai from kadai where kadainame=?", (self.kadai[kadaiidentify],))
        for i in c:
            seikai.append(i["seikai"])
        self.edit1.setPlainText(seikai[-1])  #正解ソースコードをセット


class App(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("教員用")
        global tab
        tab = MainWindow(self)
        self.addTab(tab, "MainWindow")
        
        self.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabBar().hide()
        self.resize(1260, 900)
        self.move(10,20)
        self.setStyleSheet('background-color:AliceBlue')


def move(page):
    global seitoidentify
    if page != 3:
        seitoidentify = ""

    window.removeTab(0)
    tab = MainWindow(window)
    window.addTab(tab,"MainWindow")
    window.setCurrentIndex(0)

    manual.hide()
    kadaihozon.hide()
    kadaidetail.hide()
    seitodetail.hide()

    if page == 0:
        manual.show()
    elif page == 1:
        kadaihozon.show()
    elif page == 2:
        kadaidetail.show()
    elif page == 3:
        seitodetail.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    global window
    window = App()
    window.show()
    app.exec_()