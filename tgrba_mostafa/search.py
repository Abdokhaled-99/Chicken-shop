from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from time import gmtime, strftime
import sqlite3
dig = uic.loadUi("search.ui")
dig.tableWidget.verticalHeader().hide()


dig.pushButton_6.setDisabled(True)
def disableButton():
    try:
        if len(dig.lineEdit_5.text()) > 0:
            dig.pushButton_6.setDisabled(False)
        else:
            dig.pushButton_6.setDisabled(True)
    except Exception as e :
        print(e)

dig.lineEdit_5.textChanged.connect(disableButton)



class butt(QPushButton):
    def addtable(self, x):
        try:
            dig.tableWidget.setRowCount(0)
            for  billnum,bill, total,date,time, notes,saler in x:
                r = dig.tableWidget.rowCount()
                dig.tableWidget.insertRow(r)
                dig.tableWidget.setItem(r, 0, QTableWidgetItem(str(billnum)))
                dig.tableWidget.setItem(r, 1, QTableWidgetItem(bill))
                dig.tableWidget.setItem(r, 2, QTableWidgetItem(str(total)))
                dig.tableWidget.setItem(r, 3, QTableWidgetItem(date))
                dig.tableWidget.setItem(r, 4, QTableWidgetItem(time))
                dig.tableWidget.setItem(r, 5, QTableWidgetItem(notes))

        except Exception as e:
            print(e)

    def addtable2(self, x):
        dig.tableWidget_2.setRowCount(0)
        r = dig.tableWidget_2.rowCount()
        dig.tableWidget_2.insertRow(r)
        dig.tableWidget_2.setItem(r, 0, QTableWidgetItem("\t"+str(x[0][0])))
    def search(self):
        try:
            dig.tableWidget.setRowCount(0)
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()
            prod = (dig.lineEdit_5.text(),)
            c.execute("""select *from bills where (?) in(billnum,bill,total,notes,saler)""", prod)
            x = c.fetchall()
            self.addtable(x)
            c.execute(
                """ select  sum(total) from bills where (?) in(billnum,bill,total,notes,saler)""",
                prod)
            y = c.fetchall()
            self.addtable2(y)
            c.close()
            conn.close()
        except Exception as e:
            print(e)

    def plainsearch(self):
        try:
            dig.tableWidget.setRowCount(0)
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()
            date1 = dig.dateEdit.date().toString("yyyy-MM-dd")
            date2 = dig.dateEdit_2.date().toString("yyyy-MM-dd")
            if len(dig.lineEdit_5.text()) > 0:
                c.execute(
                    """select * from bills where(?) in (billnum,bill,total,notes,saler)and date between (?) and (?) """,
                    (dig.lineEdit_5.text(), date1, date2))
                x = c.fetchall()
                self.addtable(x)
                c.execute(
                    """ select  sum(total) from bills where(?) in (billnum,bill,total,notes,saler)and date between (?) and (?) """,
                    (dig.lineEdit_5.text(), date1, date2))
                y = c.fetchall()
                self.addtable2(y)
            else:
                c.execute("""select * from bills where date between (?) and (?)""", (
                    date1, date2))
                x = c.fetchall()
                self.addtable(x)
                c.execute("""select  sum(total) from bills where date between (?) and (?)""",
                          (date1, date2))
                y = c.fetchall()
                self.addtable2(y)
            c.close()
            conn.close()
        except Exception as e:
            print(e)

    def onOpen(self):
        try:
            print("a7a")
            date = strftime("%Y-%m-%d")
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()
            c.execute("""select * from bills where date =(?)""",(date,))
            self.addtable(c.fetchall())
            c.execute("""select  sum(total) from bills where date =(?)""",(date,))
            self.addtable2(c.fetchall())
            c.close()
            conn.close()
        except Exception as e :
            print(e)
def delete():
    try:
        buttreplay = QMessageBox.question(None, "", " حذف!!!؟؟")
        if buttreplay == QMessageBox.Yes:
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()
            r = dig.tableWidget.currentRow()
            billnum = dig.tableWidget.item(r, 0).text()
            bill = dig.tableWidget.item(r, 1).text()
            total = dig.tableWidget.item(r, 2).text()
            date = dig.tableWidget.item(r, 3).text()
            time = dig.tableWidget.item(r, 4).text()
            notes = dig.tableWidget.item(r, 5).text()
            dig.tableWidget.removeRow(r)
            c.execute("""DELETE FROm bills where billnum = (?) and bill =(?) and total=(?) and date=(?) and time=(?)""", (billnum,bill,total, date,time))
            conn.commit()
            c.execute("""delete from sales where billnum=(?) and date=(?) and time=(?)""",(billnum,date,time))
            conn.commit()
            c.close()
            conn.close()
    except Exception as e:
        print(e)


b = butt()

def main():
    b.onOpen()
    dig.pushButton_4.clicked.connect(b.plainsearch)
    dig.pushButton_6.clicked.connect(b.search)
    dig.listdel.clicked.connect(delete)
    dig.show()


if __name__ == '__main__':
    main()