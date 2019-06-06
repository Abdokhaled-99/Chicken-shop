from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
import sqlite3, mobiles, prices, sales, wardat, search, hsabat
from time import gmtime, strftime

app = QtWidgets.QApplication([])
dig = uic.loadUi("3rd.ui")

dig.tableWidget.verticalHeader().hide()



saler = ""
stTime = ""
date = strftime("%Y-%m-%d")

tslem_times = 0

def search():
    try:
        conn2 = sqlite3.connect("m7l.db")
        c2 = conn2.cursor()
        saler = dig.lineEdit.text()
        c2.execute("""select  * from dorg where saler = (?)""", (saler,))
        addTotable(c2.fetchall())
    except Exception as e:
        print("dorg,search")
        print(e)

def tslem(total,Endtime):
    try:
        conn2 = sqlite3.connect("m7l.db")
        c2 = conn2.cursor()
        global tslem_times
        c2.execute("""update dorg set total = ? ,entime= ?  where saler = ? and sttime =? and [date] = ? ;""",(total,Endtime,saler,stTime,date))
        conn2.commit()
        c2.close()
        conn2.close()
    except Exception as e:
        print("dorg,tslem")
        print(e)
def tslemButt():
    total = dig.tableWidget.item(0, 3).text()
    Endtime = dig.tableWidget.item(0, 2).text()
    tslem(total,Endtime)

def searchbyDate():
    try:
        conn = sqlite3.connect("m7l.db")
        c = conn.cursor()
        date1 = dig.dateEdit.date().toString("yyyy-MM-dd")
        date2 = dig.dateEdit_2.date().toString("yyyy-MM-dd")
        saler = dig.lineEdit.text()
        if len(saler) == 0:
            # print("456")
            c.execute("""select * from dorg where date between ? and ?""",(date1,date2))

        else:
            # print("else")
            c.execute("""select * from dorg where saler =(?)and date between ? and ? """,(saler,date1,date2))
        addTotable(c.fetchall())
        c.close()
        conn.close()
    except Exception as e:
        print("dorg,searchbyDate")
        print(e)

def addTotable(x):
    try:
        dig.tableWidget.setRowCount(0)
        for saler , stTime2 , Endtime , total ,date2 in x:
            r=dig.tableWidget.rowCount()
            dig.tableWidget.insertRow(r)
            dig.tableWidget.setItem(r, 0, QTableWidgetItem(saler))
            dig.tableWidget.setItem(r, 1, QTableWidgetItem(stTime2))
            dig.tableWidget.setItem(r, 2, QTableWidgetItem(Endtime))
            dig.tableWidget.setItem(r, 3, QTableWidgetItem(str(total)))
            dig.tableWidget.setItem(r, 4, QTableWidgetItem(date2))
    except Exception as e:
        print("dorg,addTotable")
        print(e)

def select(Endtime):
    try:
        conn = sqlite3.connect("m7l2.db")
        c = conn.cursor()
        global tslem_times
        tslem_times=0
        dig.lineEdit.clear()
        c.execute("select sum(total) from bills where saler = (?) and date = (?) and  time  between (?) and (?)",
                  (saler, date, stTime, Endtime))
        x = c.fetchall()
        c.close()
        conn.close()
        total = x[0][0]
        if x[0][0] == None:
            total = 0.0
        return total
    except Exception as e :
        print(e)

def main():
    try:
        Endtime = strftime("%I:%M %p")
        total=select(Endtime)
        dig.tableWidget.setRowCount(0)
        dig.tableWidget.insertRow(0)
        dig.tableWidget.setItem(0, 0, QTableWidgetItem(saler))
        dig.tableWidget.setItem(0, 1, QTableWidgetItem(stTime))
        dig.tableWidget.setItem(0, 2, QTableWidgetItem(Endtime))
        dig.tableWidget.setItem(0, 3, QTableWidgetItem(str(total)))
        dig.tableWidget.setItem(0, 4, QTableWidgetItem(date))
        dig.show()
        app.exec()
    except Exception as e:
        print("dorg,main")
        print(e)


dig.pushButton.clicked.connect(tslemButt)
dig.pushButton_2.clicked.connect(search)
dig.pushButton_3.clicked.connect(main)
dig.pushButton_5.clicked.connect(searchbyDate)


if __name__ == '__main__':
    main()
