from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sqlite3

from time import strftime

dig = uic.loadUi("sales.ui")
dig.tableWidget.verticalHeader().hide()
dig.tableWidget_2.verticalHeader().hide()

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
            for quant, prod, price,bilnum, date,time in x:
                r = dig.tableWidget.rowCount()
                dig.tableWidget.insertRow(r)
                dig.tableWidget.setItem(r, 0, QTableWidgetItem(str(quant)))
                dig.tableWidget.setItem(r, 1, QTableWidgetItem(prod))
                dig.tableWidget.setItem(r, 2, QTableWidgetItem(str(price)))
                dig.tableWidget.setItem(r, 3, QTableWidgetItem(str(bilnum)))
                dig.tableWidget.setItem(r, 4, QTableWidgetItem(date))
        except Exception as e:
            print(e)

    def addtable2(self, x):
        dig.tableWidget_2.setRowCount(0)
        r = dig.tableWidget_2.rowCount()
        for i, n,m in x:
            dig.tableWidget_2.insertRow(r)
            dig.tableWidget_2.setItem(r, 0, QTableWidgetItem(str(i)))
            dig.tableWidget_2.setItem(r, 1, QTableWidgetItem(str(n)))
            dig.tableWidget_2.setItem(r, 2, QTableWidgetItem(str(m)))

    def search(self):
        try:
            dig.tableWidget.setRowCount(0)
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()
            prod = (dig.lineEdit_5.text(),)
            c.execute("""select *from sales where (?) in(quantity,product,price,billnum)""", prod)
            x = c.fetchall()
            self.addtable(x)
            c.execute(
                """ select sum(quantity),product,sum(price) from sales where (?) in(quantity,product,billnum)""",
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
                    """select * from sales where(?) in (quantity,product,price,billnum)and date between (?) and (?) """,
                    (dig.lineEdit_5.text(), date1, date2))
                x = c.fetchall()
                self.addtable(x)
                c.execute(
                    """ select  sum(quantity),product,sum(price) from sales where(?) in (quantity,product,price,billnum)and date between (?) and (?) group by product """,
                    (dig.lineEdit_5.text(), date1, date2))
                y = c.fetchall()
                self.addtable2(y)
            else:
                c.execute("""select * from sales where date between (?) and (?)""", (
                    date1, date2))
                x = c.fetchall()
                self.addtable(x)
                c.execute("""select  sum(quantity),product,sum(price) from sales where date between (?) and (?) group by product""",
                          (date1, date2))
                y = c.fetchall()
                self.addtable2(y)
            c.close()
            conn.close()
        except Exception as e:
            print(e)
    def onOpen(self):
        date = strftime("%Y-%m-%d")
        conn = sqlite3.connect("m7l2.db")
        c = conn.cursor()

        c.execute(
            """select  sum(quantity),product,sum(price) from sales where date = (?) group by product""",
            (date,))
        y = c.fetchall()
        self.addtable2(y)
        c.close()
        conn.close()


b=butt()
dig.pushButton_4.clicked.connect(b.plainsearch)
dig.pushButton_6.clicked.connect(b.search)
def main():
    b.onOpen()
    dig.show()
if __name__ == '__main__':
    main()