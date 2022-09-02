
import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import *

import sqlite3
import time
import linenumber

kadaiidentify = 0 #課題識別用。0：取組中の課題，1～：データベースに入れた順
seitoidentify = "" #生徒識別用。
narabi = 0 #学習者リスト並び変え用
mushi = "1"
mush = 0 #mushが1ならmushi日以前のデータを無視

conn = sqlite3.connect('data.db') #データベースファイルの場所を移動したら変更する必要アリ
conn.row_factory = sqlite3.Row
c = conn.cursor()


#表示する画面の制御(下の方に定義してあるmove関数も参照)
class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        hbox = QHBoxLayout()

        global menu
        menu = Menu(self) #画面左側のメニュー
        menu.setFrameShape(QFrame.Panel) #外枠(新しいプログラムで外枠がいらないならクラス定義でQFrameにする必要がない。teaher2.pyを参照)

        global manual
        manual = Manual(self) #マニュアル
        manual.setFrameShape(QFrame.Panel)

        global kadaihozon
        kadaihozon = KadaiHozon(self) #新規課題保存画面
        kadaihozon.setFrameShape(QFrame.Panel)

        global kadaidetail
        kadaidetail = KadaiDetail(self) #課題情報画面
        kadaidetail.setFrameShape(QFrame.Panel)

        global seitodetail
        seitodetail = SeitoDetail(self) #学習者情報画面
        seitodetail.setFrameShape(QFrame.Panel)

        hbox.addWidget(menu)
        hbox.addWidget(manual)
        hbox.addWidget(kadaihozon)
        hbox.addWidget(kadaidetail)
        hbox.addWidget(seitodetail)

        kadaihozon.hide() #一度隠す→move関数で表示を制御
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

        label1 = QLabel('課題を選択してください')
        font = QFont()
        font.setPointSize(17)
        label1.setFont(font)

        label2 = QLabel('学習者リスト')
        font = QFont()
        font.setPointSize(17)
        label2.setFont(font)

        self.edit = QLineEdit(self) #過去のデータを無視する日数を指定する用
        self.edit.setStyleSheet('background-color: white')
        font = self.edit.font()  
        font.setPointSize(20)
        self.edit.setFont(font)
        self.edit.setTextMargins(0,0,0,0)
        self.edit.setAlignment(Qt.AlignCenter)
        self.edit.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Minimum)
        self.edit.setText(mushi)

        self.check = QCheckBox(" ") #無視するか決める用
        if mush == 1:
            self.check.setChecked(True)
        self.check.clicked.connect(self.renew)

        label3 = QLabel('日以上前のデータを無視')
        font = QFont()
        font.setPointSize(17)
        label3.setFont(font)

        label4 = QLabel(' ') #レイアウト用の空白ラベル
        font = QFont()
        font.setPointSize(17)
        label4.setFont(font)

        space = QSpacerItem(100,40,QSizePolicy.Maximum,QSizePolicy.Maximum) #レイアウト用の空白

        self.combobox1 = QComboBox() #課題リストボックス
        font = QFont()
        font.setPointSize(17)
        self.combobox1.setFont(font)
        self.combobox1.setStyleSheet("background-color:white")
        kadailist = ["取り組み中の課題"] #kadailistに課題名を入れていく
        c.execute("select kadainame from kadai")
        for kadai in c:
            kadailist.append(kadai["kadainame"])
        self.combobox1.addItems(kadailist)
        self.combobox1.setCurrentIndex(kadaiidentify)
        self.combobox1.currentIndexChanged.connect(self.kadaisentaku)

        self.combobox2 = QComboBox() #並び順リストボックス
        font = QFont()
        font.setPointSize(17)
        self.combobox2.setFont(font)
        self.combobox2.setStyleSheet("background-color:white")
        sortlist = ["名前順","課題名順","状態順","躓き検出時刻が古い順"]
        self.combobox2.addItems(sortlist)
        self.combobox2.setCurrentIndex(narabi)
        self.combobox2.currentIndexChanged.connect(self.narabikae)

        table = ScrollTable(self) #学習者の表。別クラスで定義
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
        v1.addLayout(h1)
        self.setLayout(v1)


    def renew(self): #更新ボタン，無視チェックボックスのクリックで呼び出される
        global mush
        global mushi
        global seitoidentify
        if self.check.checkState(): #無視するかどうかチェックボックスで判断
            try:
                float(self.edit.text()) #バグ回避。数字のみで入力されたか判断
            except:
                message = QMessageBox()
                message.setWindowTitle("失敗")
                message.setText("数字のみで入力してください")
                okbutton = message.addButton("OK", QMessageBox.AcceptRole)
                message.setDefaultButton(okbutton)
                message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
                m = message.exec_()
            else:
                mushi = self.edit.text()
                mush = 1
        else:
            mush = 0
            mushi = self.edit.text() #無視はしないがテキスト内容は保存しておく。(moveすると消えるから)
        
        if seitoidentify == "": #学習者詳細画面以外にいる場合
            move(0)
        else: #学習者詳細画面にいる場合
            move(3)

    def kadaihozon(self): #新規課題保存ボタンで呼び出される
        move(1)

    def kadaisentaku(self): #課題リストボックスの変更で呼び出される
        global kadaiidentify
        kadaiidentify = self.combobox1.currentIndex()
        if kadaiidentify == 0: #0(取組中の課題)で課題情報画面行くとバグる
            move(0)
        else:
            move(2)

    def narabikae(self): #並び変えリストボックスの変更で呼び出される
        global narabi
        narabi = self.combobox2.currentIndex()
        move(0)

    def syuuryou(self): #終了ボタンで呼び出される
        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("終了しますか？")
        yesbutton = message.addButton("   はい   ", QMessageBox.ActionRole)
        nobutton = message.addButton("   いいえ   ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック",16, QFont.Medium))
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            QCoreApplication.instance().quit()
        elif message.clickedButton() == nobutton:
            pass
        

#学習者表の定義
class ScrollTable(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        vbox = QVBoxLayout()
        seitoset = set() #学習者のセット(被りなし)
        data = [] #表のデータを格納。rowも参照
        c.execute("select seitoname from seito")
        for i in c:
            seitoset.add(i["seitoname"]) #学習者のセットを作成

        for seito in sorted(seitoset): #学習者1人1人繰り返す。setは順番がぐちゃぐちゃなので名前順にソート
            row = [] #表の1行のみのデータを入れる→dataに入れていく(二次元配列)
            kadai = ["No Data"] #課題名
            jikan = [] #コンパイル時間
            achieve = [0] #達成状況(初期化はバグ回避)
            err = [1] #エラー有無(以前の手法の名残で，0.5がエラーあり，1以上がエラーなし)(初期化はバグ回避)
            ruiji = [0] #類似度
            comp = [] #コンパイルしたかどうか(0:課題を開いた，1:コンパイルした，-1:教員が躓き指導済みとした，2:現在)
            
            #データベース操作。学習者名，課題名で検索
            if kadaiidentify == 0: #0(取組中の課題)ならデータベースの最新のデータの課題を使う
                c.execute("select kadainame from seito where seitoname=?", (seito,))
                for i in c:
                    kadai.append(i["kadainame"])
                c.execute("select*from seito where seitoname=? and kadainame=?", (seito,kadai[-1])) #kadaiの末尾の課題名で検索
            else: #0以外ならkadaiidentifyの数によって検索
                c.execute("select kadainame from kadai")
                for i in c:
                    kadai.append(i["kadainame"]) #課題リストを作成
                c.execute("select*from seito where seitoname=? and kadainame=?", (seito,kadai[kadaiidentify]))

            kadai = ["No Data"] #kadaiidentifyの課題にまだ取り組んでいない学生を判断する用
            for i in c: #検索でヒットしたデータをリストに入れていく
                kadai.append(i["kadainame"])
                jikan.append(i["compiletime"])
                achieve.append(i["tassei"])
                err.append(i["error"])
                ruiji.append(i["simiold"]) #ここで使う類似度を設定
                comp.append(i["comp"])

            if (mush==1) and (len(jikan)>0): #mush(0 or 1)で無視するか判定，jikanはバグ回避
                if jikan[-1] < time.time()-float(mushi)*86400: #秒に換算
                    continue #以降の処理を行わず，次のループに行く→dataに入らない

            #躓き判定
            #前回のコンパイルにエラーがないなら，10分考えていたら1回，30分考えていたら更に1回カウント。初回コンパイル時は前回エラー無とする。
            #今回のコンパイルにエラーがないなら，思考時間が2分以上なら1回カウント
            #教員視点の現在時刻で学習者がエラー有のコンパイルをしたとみなす→思考時間の判定ができる
            #カウントしたタイミングで，前回のエラー無のときの類似度と，カウントしたところの時間をリストに挿入
            #3回分のカウントの間に類似度が0.05以上上昇しているものを躓きとして，その位置の時間を躓き検出時刻とする。
            simila = [] #カウントしたタイミングで類似度を入れるやつ
            unix = [] #カウントしたタイミングで時間を入れるやつ
            ruiji.append(ruiji[-1])
            jikan.append(time.time()) #現在時刻を格納
            err.append(0)
            comp.append(2) #現在を示す2を入れる
            interval = 0 #コンパイル間隔
            tumaduki = -1 #躓き判定された時間を代入する。-1は躓いていない状態を示す
            simi = 0 #類似度
            for i in range(len(jikan)):
                if comp[i] >= 1: #コンパイルしているなら
                    simi = ruiji[i+1] #類似度を更新
                    if err[i] >= 1: #前のコンパイルでエラーがないなら
                        interval = jikan[i] - jikan[i-1] #コンパイル間隔を算出
                        if interval >= 600: #思考時間が一定以上なら
                            simila.append(simi)
                            unix.append(jikan[i-1]+600)
                        if interval >= 1200: #思考時間が一定以上なら
                            simila.append(simi)
                            unix.append(jikan[i-1]+1200)
                        if interval >= 1800: #思考時間が一定以上なら
                            simila.append(simi)
                            unix.append(jikan[i-1]+1800)
                    if err[i+1] >= 1: #今のコンパイルでエラーがないなら
                        if interval > 120: #思考時間が一定以上なら
                            simila.append(simi)
                            unix.append(jikan[i])
                elif comp[i] == -1: #教員が躓きを指導済みとしたタイミング
                    simila.clear()
                    unix.clear()
                    interval = 0
            
            for i in range(2,len(simila)):
                if simila[i]-simila[i-2]<=0.05:
                    tumaduki = round((time.time() - unix[i])/60) #～分前に換算
            
            #表の状態の欄を決める
            if achieve[-1] == 1: #直近の達成状況が1なら
                state = "達成"
                tumaduki = -1 #躓き検出時刻を表示しないため
            elif comp.count(1) == 0: #リストcompの1の個数(コンパイルした回数)が0
                state = "コンパイルなし"
            elif tumaduki != -1: #躓き判定
                state = "躓き発生"
            elif err[-2] < 1: #一番最後のコンパイルのエラー
                state = "文法エラー"
            else: #他
                state = "取組中"

            
            #表の1行分のデータを入れていく
            row.append(seito)
            row.append(kadai[-1]) #kadaiの末尾(No Dataなら，検索がヒットしてない)
            row.append(state)
            row.append(tumaduki)
            if "No Data" not in row[1]:
                data.append(row) #dataに加える
        
        self.table = QTableWidget(len(data),5) #表を宣言
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

        #narabiの値によってdataを並び変える
        if narabi == 1:
            data = sorted(data,key=lambda x:x[1])
        elif narabi == 2:
            data = sorted(data,key=lambda x:x[2])
        elif narabi == 3:
            data = sorted(data,key=lambda x:x[3],reverse=True)

        #dataの値を表示する文字列に変換
        for d in data:
            d[0] = " " + str(d[0]) + " "
            d[1] = " " + str(d[1]) + " "
            d[2] = " " + str(d[2]) + " "
            if d[3] == -1:
                d[3] = " - "
            else:
                d[3] = " " + str(d[3]) + "分前 "

        for i in range(len(data)): #i行
            for j in range(len(data[i])): #j列
                self.table.setItem(i,j,QTableWidgetItem(data[i][j])) #実際に表にデータを入れる
            
            #色変え
            if " 達成 " in data[i][2]:
                self.table.item(i,2).setForeground(QColor(255,0,0))
            if " コンパイルなし " in data[i][2]:
                self.table.item(i,2).setBackground(QColor(200,200,200))
            if " 躓き発生 " in data[i][2]:
                self.table.item(i,2).setBackground(QColor(255,80,80))
            if " 文法エラー " in data[i][2]:
                self.table.item(i,2).setBackground(QColor(117,172,255))

            for j in range(len(data[i])):
                self.table.item(i,j).setTextAlignment(Qt.AlignCenter) #文字を中央揃え

            button = QPushButton("詳細")
            button.setFont(QtGui.QFont("MS　ゴシック", 15, QFont.Medium))
            button.setStyleSheet("background-color:whitesmoke")
            button.index = data[i][0].replace(" ","") #それぞれのボタンのメンバ変数としてdata[i][0](学習者名)を設定
            button.clicked.connect(self.seitodetail)
            if seitoidentify == button.index: #学習者詳細画面にいるならボタンの色を変えて分かりやすくする
                button.setStyleSheet("background-color:mediumspringgreen")
            self.table.setCellWidget(i,4,button) #実際に表にボタンを入れる
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def seitodetail(self): #詳細ボタンを押すと呼び出される
        global seitoidentify
        s = self.sender() #どのボタンによって呼び出されたか判定
        seitoidentify = s.index #押されたボタンの学習者名
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
        self.button = QPushButton("保存")
        self.button.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button.setStyleSheet("background-color:Gainsboro")
        self.button.clicked.connect(self.save)

        self.label1 = QLabel('課題名を入力してください（他の課題名と被らないようにしてください）')
        font = QFont()
        font.setPointSize(15)
        self.label1.setFont(font)

        self.label2 = QLabel('問題文を入力してください')
        font = QFont()
        font.setPointSize(15)
        self.label2.setFont(font)

        self.label3 = QLabel('正解ソースコードを入力してください')
        font = QFont()
        font.setPointSize(15)
        self.label3.setFont(font)

        self.edit1 = QLineEdit()
        self.edit1.setStyleSheet('background-color:white')
        font = self.edit1.font()  
        font.setPointSize(13)
        self.edit1.setFont(font)

        self.edit2 = QTextEdit()
        self.edit2.setStyleSheet('background-color:white')
        font = self.edit2.font()  
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.edit3 = linenumber.QCodeEditor()
        self.edit3.setStyleSheet('background-color:white')
        font = self.edit3.font()  
        font.setPointSize(13)
        self.edit3.setFont(font)

        self.check = QCheckBox('解答のひな型(設定する場合)')
        font = QFont()
        font.setPointSize(15)
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

    def template(self): #ひな型のチェックボックスが押されると呼び出し
        if self.check.checkState():
            self.edit4.show()
        else:
            self.edit4.hide()

    def save(self): #保存ボタンで呼び出される
        self.Text1 = self.edit1.text()
        self.Text2 = self.edit2.toPlainText()
        self.Text3 = self.edit3.toPlainText()
        self.Text4 = self.edit4.toPlainText()
        a = (self.Text1, self.Text2, self.Text3,self.Text4)

        #データベースに挿入
        c.execute("insert into kadai(kadainame,mondaibun,seikai,template) values(?,?,?,?)", a)
        conn.commit()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("保存しました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setDetailedText(self.Text1 + '\n\n' + self.Text2 + '\n\n' + self.Text3)
        message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
        m = message.exec_()
        move(0)


class KadaiDetail(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button1 = QPushButton("編集")
        self.button1.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button1.setStyleSheet("background-color:Gainsboro")
        self.button1.clicked.connect(self.save)

        self.button2 = QPushButton("課題削除")
        self.button2.setFont(QtGui.QFont("MS　ゴシック", 20, QFont.Medium))
        self.button2.setStyleSheet("background-color:Gainsboro")
        self.button2.clicked.connect(self.delete)

        self.label1 = QLabel('課題名（他の課題名と被らないようにしてください）')
        font = QFont()
        font.setPointSize(15)
        self.label1.setFont(font)

        self.label2 = QLabel('問題文')
        font = QFont()
        font.setPointSize(15)
        self.label2.setFont(font)

        self.label3 = QLabel('正解ソースコード')
        font = QFont()
        font.setPointSize(15)
        self.label3.setFont(font)

        self.edit1 = QLineEdit()
        self.edit1.setStyleSheet('background-color: white')
        font = self.edit1.font()  
        font.setPointSize(13)
        self.edit1.setFont(font)

        self.edit2 = QTextEdit()
        self.edit2.setStyleSheet('background-color: white')
        font = self.edit2.font()  
        font.setPointSize(13)
        self.edit2.setFont(font)

        self.edit3 = linenumber.QCodeEditor()
        self.edit3.setStyleSheet('background-color: white')
        font = self.edit3.font()
        font.setPointSize(13)
        self.edit3.setFont(font)

        self.check = QCheckBox('解答のひな型')
        font = QFont()
        font.setPointSize(15)
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

        #課題情報のリストを作る。（kadaiidentifyがリストのインデックスと合うように先頭に適当な文字を入れている）
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

        #データベースを編集
        c.execute("update kadai set kadainame=?,mondaibun=?,seikai=?,template=? where kadainame=?", a)
        c.execute("update seito set kadainame=? where kadainame=?", (self.Text1,self.text1))
        conn.commit()

        message = QMessageBox()
        message.setWindowTitle("成功")
        message.setText("編集しました")
        okbutton = message.addButton("OK", QMessageBox.AcceptRole)
        message.setDefaultButton(okbutton)
        message.setDetailedText(self.Text1 + '\n\n' + self.Text2 + '\n\n' + self.Text3)
        message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
        m = message.exec_()


    def delete(self):
        #データベースから課題情報を削除
        message = QMessageBox()
        message.setWindowTitle("確認")
        message.setText("本当に削除しますか？")
        yesbutton = message.addButton("   はい   ", QMessageBox.ActionRole)
        nobutton = message.addButton("   いいえ   ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
        m = message.exec_()

        if message.clickedButton() == yesbutton:
            c.execute("delete from kadai where kadainame=?", (self.text1,))
            c.execute("delete from seito where kadainame=?", (self.text1,))
            conn.commit()
            global kadaiidentify
            kadaiidentify = 0 #バグ避け
            move(0)
        elif message.clickedButton() == nobutton:
            pass


class SeitoDetail(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        if seitoidentify != "": #バグ避け
            self.code = [""]
            out = [""]
            ruiji = [0]
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
                ruiji.append(i["simiold"])  #ここで表示する類似度を設定

            label1 = QLabel("学習者名 ： " + str(seitoidentify))
            font = QFont()
            font.setPointSize(13)
            label1.setFont(font)

            label2 = QLabel("課題名 ： " + self.kadai[kadaiidentify])
            font = QFont()
            font.setPointSize(13)
            label2.setFont(font)

            label3 = QLabel("類似度 ： " + str(ruiji[-1]))
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

            grid = QGridLayout()
            grid.addWidget(label1,0,0,1,3)
            grid.addWidget(label2,0,3,1,3)
            grid.addWidget(label3,1,0,1,3)
            grid.addWidget(label6,2,0,1,6)
            grid.addWidget(button3,2,4,1,1)
            grid.addWidget(button4,2,5,1,1)
            grid.addWidget(self.edit1,3,0,1,6)
            grid.addWidget(label7,4,0,1,6)
            grid.addWidget(edit2,5,0,1,6)
            grid.addWidget(button1,6,0,1,3)
            grid.addWidget(button2,6,3,1,3)
            self.setLayout(grid)

    def reset(self): #躓き指導済みボタンで呼び出し。
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
        yesbutton = message.addButton("   はい   ", QMessageBox.ActionRole)
        nobutton = message.addButton("   いいえ   ", QMessageBox.ActionRole)
        message.setFont(QtGui.QFont("MS　ゴシック", 16, QFont.Medium))
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


#画面の表示切り替えをする関数
def move(page): #page引数によって表示する画面を決定
    global seitoidentify
    if page != 3:
        seitoidentify = "" #seitodetailにいない間は""にする。詳細ボタンの色，更新ボタンの移動先を制御するため

    #一度タブを消して再度タブを作る→こうしないと変数が更新されない
    window.removeTab(0)
    tab = MainWindow(window)
    window.addTab(tab,"MainWindow")
    window.setCurrentIndex(0)

    manual.hide() #一度全部隠す
    kadaihozon.hide()
    kadaidetail.hide()
    seitodetail.hide()

    if page == 0: #pageの値によって画面を表示
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