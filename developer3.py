
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
soroe = 30
soro = 0
method = "OLD"
count3 = 1800
count2 = 1200
count1 = 600
ruijijudge = 0.1
count0 = 120

conn = sqlite3.connect('data.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        hbox = QHBoxLayout()

        global menu
        menu = Menu(self)
        menu.setFrameShape(QFrame.Panel)
        menu.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Minimum)

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

        self.edit = QLineEdit()
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(20)
        self.edit.setFont(font)
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

        label5 = QLabel('カウント')
        font = QFont()
        font.setPointSize(17)
        label5.setFont(font)

        label6 = QLabel('カウントしない')
        font = QFont()
        font.setPointSize(17)
        label6.setFont(font)

        label7 = QLabel('類似度上昇')
        font = QFont()
        font.setPointSize(17)
        label7.setFont(font)

        label8 = QLabel('秒')
        font = QFont()
        font.setPointSize(17)
        label8.setFont(font)

        label9 = QLabel('秒')
        font = QFont()
        font.setPointSize(17)
        label9.setFont(font)

        label10 = QLabel('秒')
        font = QFont()
        font.setPointSize(17)
        label10.setFont(font)

        label11 = QLabel('秒')
        font = QFont()
        font.setPointSize(17)
        label11.setFont(font)

        label12 = QLabel('以上')
        font = QFont()
        font.setPointSize(17)
        label12.setFont(font)

        self.countedit3 = QLineEdit()
        self.countedit3.setStyleSheet('background-color: white')
        font = self.countedit3.font()  
        font.setPointSize(20)
        self.countedit3.setFont(font)
        self.countedit3.setAlignment(Qt.AlignCenter)
        self.countedit3.setText(str(count3))

        self.countedit2 = QLineEdit()
        self.countedit2.setStyleSheet('background-color: white')
        font = self.countedit2.font()  
        font.setPointSize(20)
        self.countedit2.setFont(font)
        self.countedit2.setAlignment(Qt.AlignCenter)
        self.countedit2.setText(str(count2))

        self.countedit1 = QLineEdit()
        self.countedit1.setStyleSheet('background-color: white')
        font = self.countedit1.font()  
        font.setPointSize(20)
        self.countedit1.setFont(font)
        self.countedit1.setAlignment(Qt.AlignCenter)
        self.countedit1.setText(str(count1))
        
        self.countedit0 = QLineEdit()
        self.countedit0.setStyleSheet('background-color: white')
        font = self.countedit0.font()  
        font.setPointSize(20)
        self.countedit0.setFont(font)
        self.countedit0.setAlignment(Qt.AlignCenter)
        self.countedit0.setText(str(count0))
        
        self.ruijiedit = QLineEdit()
        self.ruijiedit.setStyleSheet('background-color: white')
        font = self.ruijiedit.font()  
        font.setPointSize(20)
        self.ruijiedit.setFont(font)
        self.ruijiedit.setAlignment(Qt.AlignCenter)
        self.ruijiedit.setText(str(ruijijudge))

        self.check2 = QCheckBox(" ")
        if soro == 1:
            self.check2.setChecked(True)
        self.check2.clicked.connect(self.renew)

        label13 = QLabel('開始時刻を')
        font = QFont()
        font.setPointSize(17)
        label13.setFont(font)

        self.soroedit = QLineEdit()
        self.soroedit.setStyleSheet('background-color: white')
        font = self.soroedit.font()  
        font.setPointSize(20)
        self.soroedit.setFont(font)
        self.soroedit.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Minimum)
        self.soroedit.setAlignment(Qt.AlignCenter)
        self.soroedit.setText(str(soroe))

        label14 = QLabel('分前に揃える')
        font = QFont()
        font.setPointSize(17)
        label14.setFont(font)

        g1 = QGridLayout()
        g1.addWidget(label5,0,0,1,2)
        g1.addWidget(self.countedit3,0,2,1,3)
        g1.addWidget(label8,0,5,1,1)
        g1.addWidget(self.countedit2,0,6,1,3)
        g1.addWidget(label9,0,9,1,1)
        g1.addWidget(self.countedit1,0,10,1,3)
        g1.addWidget(label10,0,13,1,1)
        g1.addWidget(label6,1,0,1,2)
        g1.addWidget(self.countedit0,1,2,1,4)
        g1.addWidget(label11,1,6,1,1)
        g1.addWidget(label7,1,7,1,2)
        g1.addWidget(self.ruijiedit,1,9,1,4)
        g1.addWidget(label12,1,13,1,1)

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
        sortlist = ["名前順","課題名順","状態順","躓き検出時刻が古い順"]
        self.combobox2.addItems(sortlist)
        self.combobox2.setCurrentIndex(narabi)
        self.combobox2.currentIndexChanged.connect(self.narabikae)

        table = ScrollTable(self)
        h1 = QHBoxLayout()
        v1 = QVBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        h5 = QHBoxLayout()
        h6 = QHBoxLayout()
        h2.addWidget(label4)
        h2.addWidget(label4)
        h2.addWidget(label4)
        for i in range(3):
            h3.addWidget(label4)
        h3.addWidget(self.check)
        h2.addLayout(h3)
        h2.addWidget(self.edit)
        h2.addWidget(label3)
        for i in range(15):
            h5.addWidget(label4)
        h5.addWidget(self.check2)
        h5.addWidget(label13)
        h5.addWidget(self.soroedit)
        h5.addWidget(label14)
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
        v1.addLayout(h5)
        v1.addWidget(table)
        v1.addLayout(h4)
        v1.addLayout(g1)
        v1.addLayout(h1)
        self.setLayout(v1)


    def varenew(self):
        global count0,count1,count2,count3,ruijijudge
        try:
            int(self.countedit3.text())
            int(self.countedit2.text())
            int(self.countedit1.text())
            int(self.countedit0.text())
            float(self.ruijiedit.text())
        except:
            message = QMessageBox()
            message.setWindowTitle("失敗")
            message.setText("数字のみで入力してください")
            okbutton = message.addButton("OK", QMessageBox.AcceptRole)
            message.setDefaultButton(okbutton)
            message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
            m = message.exec_()
        else:
            count3 = int(self.countedit3.text())
            count2 = int(self.countedit2.text())
            count1 = int(self.countedit1.text())
            count0 = int(self.countedit0.text())
            ruijijudge = float(self.ruijiedit.text())

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
                message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
                m = message.exec_()
            else:
                mushi = self.edit.text()
                mush = 1
        else:
            mush = 0
            mushi = self.edit.text()

        global soro
        global soroe
        if self.check2.checkState():
            try:
                float(self.soroedit.text())
            except:
                message = QMessageBox()
                message.setWindowTitle("失敗")
                message.setText("数字のみで入力してください")
                okbutton = message.addButton("OK", QMessageBox.AcceptRole)
                message.setDefaultButton(okbutton)
                message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
                m = message.exec_()
            else:
                soroe = int(self.soroedit.text())
                soro = 1
        else:
            soro = 0
            soroe = int(self.soroedit.text())
    
    def renew(self):
        self.varenew()
        global seitoidentify
        if seitoidentify == "":
            move(0)
        else:
            move(3)

    def kadaihozon(self):
        self.varenew()
        move(1)

    def click(self):
        self.varenew()
        r = self.sender()
        global method
        method = r.text()
        global seitoidentify
        if seitoidentify == "":
            move(0)
        else:
            move(3)

    def kadaisentaku(self):
        self.varenew()
        global kadaiidentify
        kadaiidentify = self.combobox1.currentIndex()
        if kadaiidentify == 0:
            move(0)
        else:
            move(2)

    def narabikae(self):
        global narabi
        narabi = self.combobox2.currentIndex()
        self.varenew()
        move(0)

    def ignore(self):
        self.varenew()
        move(0)

    def syuuryou(self):
        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("終了しますか？")
        yesbutton = message.addButton("はい", QMessageBox.ActionRole)
        nobutton = message.addButton("いいえ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
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
            kadai = ["No Data"]
            jikan = []
            ruijiold = [0]
            ruijijaro = [0]
            ruijidc = [0]
            ruijited = [0]
            ruijito = [0]
            err = [1]
            achieve = [0]
            comp = []

            #soroが1なら，データベース検索に時間についても加える
            if kadaiidentify == 0:
                c.execute("select kadainame from seito where seitoname=?", (seito,))
                for i in c:
                    kadai.append(i["kadainame"])
                if soro == 1:
                    c.execute("select compiletime from seito where seitoname=? and kadainame=?", (seito,kadai[-1]))
                    if len(c.fetchall())>0:
                        c.execute("select compiletime from seito where seitoname=? and kadainame=?", (seito,kadai[-1]))
                        genzai = c.fetchone()[0] + soroe * 60
                        c.execute("select*from seito where seitoname=? and kadainame=? and compiletime<=?", (seito,kadai[-1],genzai))
                else:
                    c.execute("select*from seito where seitoname=? and kadainame=?", (seito,kadai[-1]))
            else:
                c.execute("select kadainame from kadai")
                for i in c:
                    kadai.append(i["kadainame"])
                if soro == 1:
                    c.execute("select compiletime from seito where seitoname=? and kadainame=?", (seito,kadai[kadaiidentify]))
                    if len(c.fetchall())>0:
                        c.execute("select compiletime from seito where seitoname=? and kadainame=?", (seito,kadai[kadaiidentify]))
                        genzai = c.fetchone()[0] + soroe * 60
                        c.execute("select*from seito where seitoname=? and kadainame=? and compiletime<=?", (seito,kadai[kadaiidentify],genzai))
                else:
                    c.execute("select*from seito where seitoname=? and kadainame=?", (seito,kadai[kadaiidentify]))

            kadai = ["No Data"]
            for i in c:
                kadai.append(i["kadainame"])
                jikan.append(i["compiletime"])
                achieve.append(i["tassei"])
                err.append(i["error"])
                ruijiold.append(i["simiold"])
                ruijijaro.append(i["simijaro"])
                ruijidc.append(i["simidc"])
                ruijited.append(i["simited"])
                ruijito.append(i["simito"])
                comp.append(i["comp"])

            if (mush==1) and (len(jikan)>0):
                if jikan[-1] < time.time()-float(mushi)*86400:
                    continue

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

            simila = []
            unix = []
            simimethod = [ruijiold,ruijijaro,ruijidc,ruijited,ruijito]
            for s in simimethod:
                s.append(s[-1])
            if (soro == 1)and(len(jikan)>0): #一番最初に課題を開いたタイミングをsoroe分前とする。
                sabun = time.time() - soroe * 60 - jikan[0]
                for i in range(len(jikan)):
                    jikan[i] = jikan[i] + sabun
            jikan.append(time.time())
            err.append(0)
            comp.append(2)
            interval = 0
            tumaduki = -1
            simi = 0
            for i in range(len(jikan)):
                if comp[i] >= 1:
                    simi = ruiji[i+1]
                    if err[i] >= 1:
                        interval = jikan[i] - jikan[i-1]
                        if interval >= count1:
                            simila.append(simi)
                            unix.append(jikan[i-1] + count1)
                        if interval >= count2:
                            simila.append(simi)
                            unix.append(jikan[i-1] + count2)
                        if interval >= count3:
                            simila.append(simi)
                            unix.append(jikan[i-1] + count3)
                    if err[i+1] >= 1:
                        if interval > count0:
                            simila.append(simi)
                            unix.append(jikan[i])
                elif comp[i] == -1:
                    simila.clear()
                    unix.clear()
                    interval = 0
            
            for i in range(2,len(simila)):
                if simila[i]-simila[i-2]<=ruijijudge:
                    tumaduki = round((time.time() - unix[i])/60)
            
            if achieve[-1] == 1:
                state = "達成"
                tumaduki = -1
            elif tumaduki != -1:
                state = "躓き発生"
            elif comp.count(1) == 0:
                state = "コンパイルなし"
            elif err[-2] < 1:
                state = "文法エラー"
            else:
                state = "取組中"

            row.append(seito)
            row.append(kadai[-1])
            row.append(state)
            row.append(tumaduki)
            if "No Data" not in row[1]:
                data.append(row)
        
        self.table = QTableWidget(len(data),5)
        self.table.setStyleSheet("background-color: White")
        self.table.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)
        self.table.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = ["学習者名","課題名","状態","躓き検出時刻",""]
        self.table.setHorizontalHeaderLabels(header)
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents)
        if narabi == 1:
            data = sorted(data,key=lambda x:x[1])
        elif narabi == 2:
            data = sorted(data,key=lambda x:x[2])
        elif narabi == 3:
            data = sorted(data,key=lambda x:x[3],reverse=True)

        for d in data:
            d[0] = " " + str(d[0]) + " "
            d[1] = " " + str(d[1]) + " "
            d[2] = " " + str(d[2]) + " "
            if d[3] == -1:
                d[3] = " - "
            else:
                d[3] = " " + str(d[3]) + "分前 "

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.table.setItem(i,j,QTableWidgetItem(data[i][j]))
            if " 達成 " in data[i][2]:
                self.table.item(i,2).setForeground(QColor(255,0,0))
            if " コンパイルなし " in data[i][2]:
                self.table.item(i,2).setBackground(QColor(200,200,200))
            if " 躓き発生 " in data[i][2]:
                self.table.item(i,2).setBackground(QColor(255,80,80))
            if " 文法エラー " in data[i][2]:
                self.table.item(i,2).setBackground(QColor(117,172,255))
            for j in range(len(data[i])):
                self.table.item(i,j).setTextAlignment(Qt.AlignCenter)

            button = QPushButton("詳細")
            button.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))
            button.setStyleSheet("background-color:whitesmoke")
            button.index = data[i][0].replace(" ","")
            button.clicked.connect(self.seitodetail)
            if seitoidentify == button.index:
                button.setStyleSheet("background-color:mediumspringgreen")
            self.table.setCellWidget(i,4,button)
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

        l = QLabel("マニュアル",self)
        font = QFont()
        font.setPointSize(17)
        l.setFont(font)
        l.move(265,10)

        label1 = QLabel("課題を選ぶと詳細が表示されます。\n課題の編集・削除が可能です。")
        font = QFont()
        font.setPointSize(15)
        label1.setFont(font)

        label2 = QLabel("学習者リストを指定の方法で並び変えることができます。\n\nテキストボックスに実数を入力してチェックを入れると\n指定した日数以前のデータが表示されなくなります。")
        font = QFont()
        font.setPointSize(15)
        label2.setFont(font)

        label3 = QLabel("状態")
        font = QFont()
        font.setPointSize(15)
        label3.setFont(font)

        label4 = QLabel("：ロジック構成面の躓きが発生したと推測されます")
        font = QFont()
        font.setPointSize(15)
        label4.setFont(font)

        label5 = QLabel()
        image = QImage("tsumaduki.png")
        label5.setPixmap(QPixmap.fromImage(image))

        label6 = QLabel("：文法的に躓いている可能性があります")
        font = QFont()
        font.setPointSize(15)
        label6.setFont(font)

        label7 = QLabel()
        image = QImage("bunpouerror.png")
        label7.setPixmap(QPixmap.fromImage(image))

        label8 = QLabel("：まだ一度もコンパイルがされていない状態です")
        font = QFont()
        font.setPointSize(15)
        label8.setFont(font)

        label9 = QLabel()
        image = QImage("compilenashi.png")
        label9.setPixmap(QPixmap.fromImage(image))

        label10 = QLabel("：学習者により課題が達成とされています")
        font = QFont()
        font.setPointSize(15)
        label10.setFont(font)

        label11 = QLabel()
        image = QImage("tassei.png")
        label11.setPixmap(QPixmap.fromImage(image))

        label12 = QLabel("：上記以外の学生です")
        font = QFont()
        font.setPointSize(15)
        label12.setFont(font)

        label13 = QLabel()
        image = QImage("torikumityu.png")
        label13.setPixmap(QPixmap.fromImage(image))

        label15 = QLabel("更新：画面を更新\n新規課題保存：新しい課題をデータベースに保存\n終了：アプリを終了")
        font = QFont()
        font.setPointSize(15)
        label15.setFont(font)

        label16 = QLabel()
        image = QImage("shousai.png")
        label16.setPixmap(QPixmap.fromImage(image))

        label17 = QLabel("を押すと学習者の詳細な状況を閲覧できます。")
        font = QFont()
        font.setPointSize(15)
        label17.setFont(font)

        label22 = QLabel()
        image = QImage("shidouzumi.png")
        label22.setPixmap(QPixmap.fromImage(image))

        label23 = QLabel("を押すと参照中の学習者の躓き情報をリセットできます。")
        font = QFont()
        font.setPointSize(15)
        label23.setFont(font)

        label24 = QLabel()
        image = QImage("gakusyusyasakujo.png")
        label24.setPixmap(QPixmap.fromImage(image))

        label25 = QLabel("を押すと参照中の学習者情報を削除できます。")
        font = QFont()
        font.setPointSize(15)
        label25.setFont(font)

        v = QVBoxLayout()
        g1 = QGridLayout()
        g2 = QGridLayout()
        space = QSpacerItem(100,60,QSizePolicy.Maximum,QSizePolicy.Maximum)
        v.addSpacerItem(space)
        v.addWidget(label1)
        v.addSpacerItem(space)
        v.addWidget(label2)
        v.addStretch(1)
        v.addWidget(label3)
        g1.addWidget(label5,0,0,1,1)
        g1.addWidget(label4,0,1,1,4)
        g1.addWidget(label7,1,0,1,1)
        g1.addWidget(label6,1,1,1,4)
        g1.addWidget(label9,2,0,1,1)
        g1.addWidget(label8,2,1,1,4)
        g1.addWidget(label11,3,0,1,1)
        g1.addWidget(label10,3,1,1,4)
        g1.addWidget(label13,4,0,1,1)
        g1.addWidget(label12,4,1,1,4)
        v.addLayout(g1)
        v.addStretch(1)
        v.addStretch(1)
        g2.addWidget(label16,0,0,1,1)
        g2.addWidget(label17,0,1,1,6)
        g2.addWidget(label22,1,0,1,1)
        g2.addWidget(label23,1,1,1,6)
        g2.addWidget(label24,2,0,1,1)
        g2.addWidget(label25,2,1,1,6)
        v.addLayout(g2)
        v.addStretch(1)
        v.addWidget(label15)
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

        self.check = QCheckBox('解答のひな型(設定する場合)')
        font = QFont()
        font.setPointSize(12)
        self.check.setFont(font)
        self.check.clicked.connect(self.template)

        self.edit4 = linenumber.QCodeEditor()
        self.edit4.setStyleSheet('background-color:white')
        font = self.edit4.font()  
        font.setPointSize(13)
        self.edit4.setFont(font)

        grid = QGridLayout()

        grid.addWidget(self.label1,0,0,1,2)
        grid.addWidget(self.edit1,1,0,1,2)
        grid.addWidget(self.label2,2,0,1,2)
        grid.addWidget(self.edit2,3,0,1,2)
        grid.addWidget(self.label3,4,0,1,2)
        grid.addWidget(self.edit3,5,0,1,2)
        grid.addWidget(self.check,6,0,1,2)
        grid.addWidget(self.edit4,7,0,1,2)
        grid.addWidget(self.button,8,0,1,2)
        self.setLayout(grid)
        self.edit4.hide()

    def template(self):
        if self.check.checkState():
            self.edit4.show()
        else:
            self.edit4.hide()

    def save(self):
        self.Text1 = self.edit1.text()
        self.Text2 = self.edit2.toPlainText()
        self.Text3 = self.edit3.toPlainText()
        self.Text4 = self.edit4.toPlainText()
        a = (self.Text1, self.Text2, self.Text3, self.Text4)

        c.execute("insert into kadai(kadainame,mondaibun,seikai,template) values(?,?,?,?)", a)
        conn.commit()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("保存しました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setDetailedText(self.Text1 + '\n\n' + self.Text2 + '\n\n' + self.Text3)
        message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
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

        self.check = QCheckBox('解答のひな型')
        font = QFont()
        font.setPointSize(12)
        self.check.setFont(font)
        self.check.clicked.connect(self.template)

        self.edit4 = linenumber.QCodeEditor()
        self.edit4.setStyleSheet('background-color:white')
        font = self.edit4.font()  
        font.setPointSize(13)
        self.edit4.setFont(font)

        grid = QGridLayout()

        grid.addWidget(self.label1, 0, 0, 1, 2)
        grid.addWidget(self.edit1, 1, 0, 1, 2)
        grid.addWidget(self.label2, 2, 0, 1, 2)
        grid.addWidget(self.edit2, 3, 0, 1, 2)
        grid.addWidget(self.label3, 4, 0, 1, 2)
        grid.addWidget(self.edit3, 5, 0, 1, 2)
        grid.addWidget(self.check,6,0,1,2)
        grid.addWidget(self.edit4,7,0,1,2)
        grid.addWidget(self.button1, 8, 0, 1, 1)
        grid.addWidget(self.button2, 8, 1, 1, 1)
        self.setLayout(grid)
        self.edit4.hide()

        list1=["課題名",]
        list2=["問題文",]
        list3=["正解",]
        list4=["解答のひな型",]

        c.execute("select*from kadai")
        for i in c:
            list1.append(i["kadainame"])
            list2.append(i["mondaibun"])
            list3.append(i["seikai"])
            list4.append(i["template"])

        self.text1 = list1[kadaiidentify]
        self.text2 = list2[kadaiidentify]
        self.text3 = list3[kadaiidentify]
        self.text4 = list4[kadaiidentify]

        self.edit1.setText(self.text1)
        self.edit2.setPlainText(self.text2)
        self.edit3.setPlainText(self.text3)
        self.edit4.setPlainText(self.text4)
        
    def template(self):
        if self.check.checkState():
            self.edit4.show()
        else:
            self.edit4.hide()

    def save(self):
        self.Text1 = self.edit1.text()
        self.Text2 = self.edit2.toPlainText()
        self.Text3 = self.edit3.toPlainText()
        self.Text4 = self.edit4.toPlainText()
        a = (self.Text1, self.Text2, self.Text3, self.Text4, self.text1)

        c.execute("update kadai set kadainame=?,mondaibun=?,seikai=?,template=? where kadainame=?", a)
        conn.commit()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("編集しました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setDetailedText(self.Text1 + '\n\n' + self.Text2 + '\n\n' + self.Text3)
        message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
        m = message.exec_()


    def delete(self):

        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("本当に削除しますか？")
        yesbutton = message.addButton("はい", QMessageBox.ActionRole)
        nobutton = message.addButton("いいえ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
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
        c.execute("select kadainame from seito where seitoname=?", (seitoidentify,))
        for i in c:
            kadailist.append(i["kadainame"])
        kadai.append(kadailist[-1])
        c.execute("select kadainame from kadai")
        for i in c:
            kadai.append(i["kadainame"])
        if soro == 1:
            c.execute("select compiletime from seito where seitoname=? and kadainame=?", (seitoidentify,kadai[kadaiidentify]))
            genzai = c.fetchone()[0] + soroe * 60
            c.execute("select*from seito where seitoname=? and kadainame=? and compiletime<=?", (seitoidentify,kadai[kadaiidentify],genzai))
        else:
            c.execute("select*from seito where seitoname=? and kadainame=?", (seitoidentify,kadai[kadaiidentify]))
        for i in c:
            ruijiold.append(i["simiold"])
            ruijijaro.append(i["simijaro"])
            ruijidc.append(i["simidc"])
            ruijited.append(i["simited"])
            ruijito.append(i["simito"])
            err.append(i["error"])
            achieve.append(i["tassei"])
            jikan.append(i["compiletime"])
            comp.append(i["comp"])

        simimethod = [ruijiold,ruijijaro,ruijidc,ruijited,ruijito]
        for s in simimethod:
            s.append(s[-1])
        if (soro == 1)and(len(jikan)>0):
                sabun = time.time() - soroe * 60 - jikan[0]
                for i in range(len(jikan)):
                    jikan[i] = jikan[i] + sabun
        jikan.append(time.time())
        err.append(0)
        comp.append(2)
        judge = 0
        interval = 0
        for i in range(len(jikan)):
            row = []
            row.append(comp[i])
            if comp[i] >= 1:
                #row.append(round((jikan[i]-jikan[i-1])/60))
                row.append(round(jikan[i]-jikan[i-1]))
                if err[i]>=1:
                    interval = jikan[i] - jikan[i-1]
                    if interval >= count1:
                        judge = judge + 1
                    if interval >= count2:
                        judge = judge + 1
                    if interval >= count3:
                        judge = judge + 1
            else:
                row.append("-")
                if comp[i] == -1:
                    interval = 0
                    judge = 0
            if err[i+1]==0:
                row.append("-")
            elif err[i+1]<1:
                row.append("有")
            elif err[i+1]>=1:
                row.append("無")
                if interval > count0:
                    judge=judge+1
            row.append(judge)
            for k,s in enumerate(simimethod):
                row.append(s[i+1])
            data.append(row)

        self.table = QTableWidget(len(data),9)
        self.table.setStyleSheet("background-color: White")
        self.table.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)
        self.table.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = ["コンパイル","間隔","エラー","判定","OLD","Jaro","DC","TED","TO"]
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

        for d in data:
            d[0] = " " + str(d[0]) + " "
            d[1] = " " + str(d[1]) + "秒 "
            d[2] = " " + str(d[2]) + " "
            d[3] = " " + str(d[3]) + " "
            d[4] = " " + str(d[4]) + " "
            d[5] = " " + str(d[5]) + " "
            d[6] = " " + str(d[6]) + " "
            d[7] = " " + str(d[7]) + " "
            d[8] = " " + str(d[8]) + " "

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.table.setItem(i,j,QTableWidgetItem(data[i][j]))
            if " 無 " in data[i][2]:
                self.table.item(i,2).setForeground(QColor(0,0,255))
            elif " 有 " in data[i][2]:
                self.table.item(i,2).setForeground(QColor(255,0,0))
            for j in range(len(data[i])):
                self.table.item(i,j).setTextAlignment(Qt.AlignCenter)
        vbox.addWidget(self.table)
        self.setLayout(vbox)


class SeitoDetail(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        if seitoidentify != "":
            self.code = [""]
            out = [""]
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

            button1 = QPushButton("躓き指導済")
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
            grid.addWidget(label3,2,0,1,3)
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
        c.execute("select * from seito where seitoname=? and kadainame=?", a)
        for i in c:
            res1 = i["seitoname"]
            res2 = i["kadainame"]
            res3 = i["sourcecode"]
            res4 = i["output"]
            res5 = i["compiletime"]
            res6 = i["simiold"]
            res7 = i["simijaro"]
            res8 = i["simidc"]
            res9 = i["simited"]
            res10 = i["simito"]
            res11 = i["error"]
            res12 = i["judgeparameter"]
            res13 = i["tassei"]
        a = (res1,res2,res3,res4,res5,res6,res7,res8,res9,res10,res11,res12,res13)
        c.execute("insert into seito (seitoname,kadainame,sourcecode,output,compiletime,simiold,simijaro,simidc,simited,simito,error,judgeparameter,tassei,comp) values(?,?,?,?,?,?,?,?,?,?,?,?,?,-1)", a)
        conn.commit()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("躓きをリセットしました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
        m = message.exec_()

        move(3)

    def delete(self):

        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("本当に削除しますか？")
        yesbutton = message.addButton("はい", QMessageBox.ActionRole)
        nobutton = message.addButton("いいえ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
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