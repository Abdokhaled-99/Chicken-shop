from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from time import gmtime, strftime
import sqlite3

dig = uic.loadUi("wardat.ui")
dig.tableWidget.verticalHeader().hide()
dig.tableWidget_2.verticalHeader().hide()

dig.name.hide()
dig.change.hide()
dig.price.hide()
dig.product.hide()
dig.quant.hide()
dig.notes.hide()
dig.pushButton.hide()
dig.label.hide()
dig.label_2.hide()
dig.label_3.hide()
dig.label_4.hide()
dig.label_5.hide()
dig.label_8.hide()

dig.dateEdit.hide()
dig.dateEdit_2.hide()
dig.label_6.hide()
dig.label_7.hide()
dig.lineEdit_5.hide()
dig.pushButton_4.hide()
dig.pushButton_6.hide()
dig.listdel.hide()
dig.tableWidget_2.hide()

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


def clearadds():
    dig.quant.clear()
    dig.product.clear()
    dig.price.clear()
    dig.name.clear()
    dig.change.clear()
    dig.notes.clear()


def addtotable():
    try:
        dig.tableWidget.setRowCount(0)
        conn = sqlite3.connect("m7l.db")
        c = conn.cursor()
        quant = dig.quant.text()
        prod = dig.product.text()
        price = dig.price.text()
        name = dig.name.text()

        notes = dig.notes.text()
        change = dig.change.text()
        date = strftime("%Y-%m-%d")
        time = strftime("%I:%M %p")
        c.execute("""insert into wardat (quantity,product,price,name,[date],notes,change) values (?,?,?,?,?,?,?); """
                  , (quant, prod, price, name, date, notes,change))
        conn.commit()
        c.close()
        conn.close()
        r = dig.tableWidget.rowCount()
        dig.tableWidget.insertRow(r)
        dig.tableWidget.setItem(r, 0, QTableWidgetItem(quant))
        dig.tableWidget.setItem(r, 1, QTableWidgetItem(prod))
        dig.tableWidget.setItem(r, 2, QTableWidgetItem(name))
        dig.tableWidget.setItem(r, 3, QTableWidgetItem(price))
        dig.tableWidget.setItem(r, 4, QTableWidgetItem(change))
        dig.tableWidget.setItem(r, 5, QTableWidgetItem(date))
        dig.tableWidget.setItem(r, 6, QTableWidgetItem(notes))
        clearadds()
    except Exception as e:
        print(e)


class butt(QPushButton):
    def addtable(self, x):
        try:
            dig.tableWidget.setRowCount(0)
            for quant, prod, price, name, date, notes,change in x:
                r = dig.tableWidget.rowCount()
                dig.tableWidget.insertRow(r)
                dig.tableWidget.setItem(r, 0, QTableWidgetItem(str(quant)))
                dig.tableWidget.setItem(r, 1, QTableWidgetItem(prod))
                dig.tableWidget.setItem(r, 2, QTableWidgetItem(name))
                dig.tableWidget.setItem(r, 3, QTableWidgetItem(str(price)))
                dig.tableWidget.setItem(r, 4, QTableWidgetItem(str(change)))
                dig.tableWidget.setItem(r, 5, QTableWidgetItem(date))
                dig.tableWidget.setItem(r, 6, QTableWidgetItem(notes))
        except Exception as e:
            print(e)

    def addtable2(self, x):
        dig.tableWidget_2.setRowCount(0)
        r = dig.tableWidget_2.rowCount()
        for q,n, prd,prc,ch in x:
            dig.tableWidget_2.insertRow(r)
            dig.tableWidget_2.setItem(r, 0, QTableWidgetItem(str(q)))
            dig.tableWidget_2.setItem(r, 1, QTableWidgetItem("    "+n))
            dig.tableWidget_2.setItem(r, 2, QTableWidgetItem(str(prd)))
            dig.tableWidget_2.setItem(r, 3, QTableWidgetItem(str(prc)))
            dig.tableWidget_2.setItem(r, 4, QTableWidgetItem(str(ch)))

    def onOpen(self):
        conn = sqlite3.connect("m7l.db")
        c = conn.cursor()
        date = strftime("%Y-%m-%d")
        c.execute("""select sum(quantity),name,product,sum(price),sum(change) from wardat where date = (?) group by name,product;""", (date,))
        result = c.fetchall()
        c.close()
        conn.close()
        # print(result)
        self.addtable2(result)
    def search(self):
        try:
            dig.tableWidget.setRowCount(0)
            conn = sqlite3.connect("m7l.db")
            c = conn.cursor()
            prod = (dig.lineEdit_5.text(),)
            c.execute("""select *from wardat where (?) in(quantity,product,price,name,change,notes)""", prod)
            x = c.fetchall()
            self.addtable(x)
            c.execute(
                """ select sum(quantity),name,product,sum(price),sum(change) from wardat where (?) in(quantity,product,price,name,notes) GROUP BY name,product""",
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
            conn = sqlite3.connect("m7l.db")
            c = conn.cursor()
            date1 = dig.dateEdit.date().toString("yyyy-MM-dd")
            date2 = dig.dateEdit_2.date().toString("yyyy-MM-dd")
            if len(dig.lineEdit_5.text()) > 0:
                c.execute(
                    """select * from wardat where(?) in (quantity,product,price,name,notes)and date between (?) and (?) """,
                    (dig.lineEdit_5.text(), date1, date2))
                x = c.fetchall()
                self.addtable(x)
                c.execute(
                    """ select  sum(quantity),name,product,sum(price),sum(change) from wardat where(?) in (quantity,product,price,name,notes)and date between (?) and (?) group by name""",
                    (dig.lineEdit_5.text(), date1, date2))
                y = c.fetchall()
                self.addtable2(y)
            else:
                c.execute("""select * from wardat where date between (?) and (?)""", (
                    date1, date2))
                x = c.fetchall()
                self.addtable(x)
                c.execute("""select  sum(quantity),name,product,sum(price),sum(change) from wardat where date between (?) and (?) group by name""",
                          (date1, date2))
                y = c.fetchall()
                self.addtable2(y)
            c.close()
            conn.close()
        except Exception as e:
            print(e)


def delete():
    try:
        buttreplay = QMessageBox.question(None, "", " حذف!!!؟؟")
        if buttreplay == QMessageBox.Yes:
            conn = sqlite3.connect("m7l.db")
            c = conn.cursor()
            r = dig.tableWidget.currentRow()
            quan = dig.tableWidget.item(r, 0).text()
            prod = dig.tableWidget.item(r, 1).text()
            name = dig.tableWidget.item(r, 2).text()
            price = dig.tableWidget.item(r, 3).text()
            date = dig.tableWidget.item(r, 5).text()
            notes = dig.tableWidget.item(r, 6).text()
            dig.tableWidget.removeRow(r)
            c.execute("""DELETE FROm wardat where quantity = (?) and product =(?) and price=(?) and name=(?) and date=(?)
    and notes = (?)""", (quan, prod, price, name, date, notes))
            conn.commit()
            c.close()
            conn.close()
    except Exception as e:
        print(e)




b = butt()

dig.pushButton.clicked.connect(addtotable)
dig.pushButton_4.clicked.connect(b.plainsearch)
dig.pushButton_6.clicked.connect(b.search)
dig.listdel.clicked.connect(delete)
dig.pushButton_5.clicked.connect(b.onOpen)
# dig.pushButton_5.clicked.connect(b.onOpen)
def main():
    dig.show()
if __name__ == '__main__':
    main()
