from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import *
from time import gmtime, strftime
import sqlite3
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

# app = QtWidgets.QApplication([])
dig = uic.loadUi("hsabat.ui")
dig.tableWidget.verticalHeader().hide()
dig.textEdit.hide()


dig.pushButton.setDisabled(True)

dig.tableWidget.setColumnWidth(1, 190)

def disableButton():
    try:
        if len(dig.lineEdit.text()) > 0:
            dig.pushButton.setDisabled(False)
        else:
            dig.pushButton.setDisabled(True)
    except Exception as e :
        print(e)

dig.lineEdit.textChanged.connect(disableButton)



class butt(QPushButton):

    def createPrinteDialog(self,bill):
        try:
            printer = QPrinter(QPrinter.ScreenResolution)
            printer.setPageSize(30)
            printer.setFullPage(True)
            painter = QPainter()
            painter.begin(printer)
            painter.setFont(QFont("Segoe UI", 10, 1500))
            painter.drawText(230, 30, 0, 2000,Qt.TextIncludeTrailingSpaces | Qt.AlignRight, bill)
            painter.end()
            # print(bill)
        except Exception as e:
            print(e)

    def search(self):
        try:
            sender =self.sender().text()

            dig.tableWidget.setRowCount(0)
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()

            prod = dig.lineEdit.text()
            if sender == "بحث بالتاريخ":
                date1 = dig.dateEdit.date().toString("yyyy-MM-dd")
                date2 = dig.dateEdit_2.date().toString("yyyy-MM-dd")
                if len(prod) > 0:
                    c.execute(
                        """select * from dyon where(?) in (billnum,bill,total,notes,saler,customer)and date between (?) and (?) """,
                        (prod, date1, date2))
                else:
                    c.execute("""select * from dyon where date between (?) and (?)""", (
                        date1, date2))
            else:
                c.execute("""select * from dyon where (?) in (billnum,bill,total,notes,saler,customer)""",( prod,))
            x = c.fetchall()
            self.addTotable(x)
        except Exception as e:
            print(e)
    def addTotable(self,x):
        try:
            dig.tableWidget.setRowCount(0)
            for bn, b, t, date, time, notes, saler,customer,mobile in x:
                r = dig.tableWidget.rowCount()
                dig.tableWidget.insertRow(r)
                dig.tableWidget.setItem(r, 0, QTableWidgetItem(bn))
                dig.tableWidget.setItem(r, 1, QTableWidgetItem(b))
                dig.tableWidget.setItem(r, 2, QTableWidgetItem(str(t)))
                dig.tableWidget.setItem(r, 3, QTableWidgetItem(customer))
                dig.tableWidget.setItem(r, 4, QTableWidgetItem(mobile))
                dig.tableWidget.setItem(r, 5, QTableWidgetItem(date))
                dig.tableWidget.setItem(r, 6, QTableWidgetItem(time))
                dig.tableWidget.setItem(r, 7, QTableWidgetItem(notes))
                dig.tableWidget.setItem(r, 8, QTableWidgetItem(saler))

        except Exception as e :
            print(e)
    def onOpen(self):
        try:
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()
            date = strftime("%Y-%m-%d")
            c.execute("""select * from dyon where date = (?) group by customer,saler order by time ;""", (date,))
            result = c.fetchall()
            c.close()
            conn.close()
            # print(result)
            self.addTotable(result)
        except Exception as e :
            print(e)
    def dele(self):
        try:
            sender = self.sender().text()
            conn = sqlite3.connect("m7l2.db")
            c = conn.cursor()
            r = dig.tableWidget.currentRow()
            billnum = dig.tableWidget.item(r, 0).text()
            bill = dig.tableWidget.item(r, 1).text()
            total = dig.tableWidget.item(r, 2).text()
            # customer = dig.tableWidget.item(r, 3).text()
            mobile = dig.tableWidget.item(r, 4).text()
            date = dig.tableWidget.item(r, 5).text()
            time = dig.tableWidget.item(r, 6).text()
            notes = dig.tableWidget.item(r, 7).text()
            saler = dig.tableWidget.item(r, 8).text()

            if sender == "حذف":
                buttreplay = QMessageBox.question(None, "", " حذف!!!؟؟")
                if buttreplay == QMessageBox.Yes:
                    dig.tableWidget.removeRow(r)

                    c.execute(
                        """DELETE FROm dyon where billnum = (?) and bill =(?) and total=(?) and date=(?) and time=(?)""",
                        (billnum, bill, total, date, time))
                    conn.commit()
                    c.execute("""delete from sales where billnum = (?) and date =(?) and time=(?)""",(billnum,date,time))
                    conn.commit()
            else:
                bill2 ="طيور المصطفى"+"\n"+"\t٠١٠٩٣٨٨٩٣٣١,٠١١٢٧٧٨١٣٥٦"+"\n"+"رقم الفاتورة\t {}".format(billnum)+"\n"+"الوزن   \t   السلعة\t     السعر\t"+"\n" + bill +"\n====================================================================\n"+"الاجمالي : {} ".format(total)+"\n{}\t{}".format(date, time)
                self.createPrinteDialog(bill2)
                dig.tableWidget.removeRow(r)
                c.execute(
                    """DELETE FROm dyon where billnum = (?) and bill =(?) and total=(?) and date=(?) and time=(?)""",
                    (billnum, bill, total, date, time))
                conn.commit()

                c.execute("""insert into bills (billnum,bill,total,[date],[time],notes,saler) values (?,?,?,?,?,?,?);""",
                          (billnum, bill, total, date, time, notes,saler))
                conn.commit()
            c.close()
            conn.close()


        except Exception as e:
            print(e)


b = butt()
dig.pushButton.clicked.connect(b.search)
dig.pushButton_7.clicked.connect(b.search)
dig.pushButton_3.clicked.connect(b.dele)
dig.pushButton_2.clicked.connect(b.dele)
def main():
    b.onOpen()
    dig.show()


if __name__ == '__main__':
    main()