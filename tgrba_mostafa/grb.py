import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtPrintSupport import QPrinter
import sqlite3, mobiles, prices, sales, wardat, search, hsabat, dorg,Elmostafa

from PyQt5 import uic, QtCore

from PyQt5.QtWidgets import *

from time import strftime


class MainWindow(QMainWindow):
    def __init__(self,name,id,strtime):
        self.name=name
        self.strtime=strtime
        # name, strtime = "a7a",5
        QMainWindow.__init__(self)
        dig = uic.loadUi('main.ui', self)
        dig.label_7.setText(name)
        dig.textBrowser.hide()
        dig.scrollArea.hide()
        dig.scrollArea_2.hide()
        dig.tableWidget.setColumnWidth(0, 80)
        dig.tableWidget.setColumnWidth(4, 50)
        dig.tableWidget.setColumnWidth(1, 230)
        dig.tableWidget.setColumnWidth(2, 90)
        dig.tableWidget.verticalHeader().hide()
        dig.label_4.hide()
        dig.dele.setDisabled(True)

        def putter():
            dig.bill.clear()
            date = strftime("%Y-%m-%d")
            conn = sqlite3.connect("m7l.db")
            c = conn.cursor()
            c.execute("""select max(cast(billnum as INTEGER)) from bills  where date=(?)  """, (date,))
            num = c.fetchone()
            if num[0]:
                x = int(num[0]) + 1
            else:
                x = "1"
            dig.label_4.setText(str(x))
            dig.bill.addItem("طيور المصطفى")
            dig.bill.addItem("٠١٠٩٣٨٨٩٣٣١,٠١١٢٧٧٨١٣٥٦")
            dig.bill.addItem("رقم الفاتورة\t {}".format(x))
            dig.bill.addItem("{}\t{}\t{}".format("الوزن", "السلعة", "السعر"))

        putter()

        def disableButton():
            if len(dig.screen.text()) > 0:
                dig.dele.setDisabled(False)

            else:


                dig.dele.setDisabled(True)

        dig.screen.textChanged.connect(disableButton)

        class butt(QPushButton):
            saler = name
            stTime = strtime
            quant = ""
            total = 0
            z = []

            def calc(self):
                try:
                    if self.sender().text() == "c":
                        dig.screen.clear()
                        self.quant = ""
                    elif self.sender().text() == "del":
                        self.quant = self.quant[:len(self.quant) - 1]
                        dig.screen.setText(self.quant)
                    else:
                        self.quant += self.sender().text()
                        dig.screen.setText(self.quant)
                except Exception as e:
                    print(e)

            def defulty(self, prod):
                try:
                    if self.quant == "":
                        QMessageBox.information(None, "Error", "ادخل الكمية من فضلك !!")
                    else:
                        billnum = dig.label_4.text()
                        qun = 1
                        if self.quant.__contains__("x"):
                            splity = self.quant.split("x")
                            for i in splity:
                                if i == "":
                                    continue
                                else:
                                    qun*=float(i)
                        else:
                            qun = float(self.quant)
                        conn = sqlite3.connect("m7l.db")
                        c = conn.cursor()
                        c.execute("""select price from meneu where product = (?)""", ((prod,)))
                        price = c.fetchone()[0]
                        c.close()
                        conn.close()
                        self.total += qun * float(price)
                        dig.label_5.setText(str(self.total))
                        dig.bill.addItem(
                            "{}\t{}\t{} × {} =\t{} ".format(str(qun), prod, str(qun), price, str(qun * float(price))))
                        dig.screen.clear()
                        self.z.append([qun, prod, float(qun) * float(price), billnum])
                        self.quant = ""
                except Exception as e:
                    print("defualty")
                    print(e)

            def billing(self):
                try:
                    prod = self.sender().text()
                    self.defulty(prod)
                except Exception as e:
                    print(e)

            def combobox(self, prod):
                try:

                    self.defulty(prod)
                except Exception as e:
                    print("combobox")
                    print(e)

            def additem(self):
                try:
                    billnum = dig.label_4.text()
                    qun = float(dig.weight.text())
                    prod = dig.item.text()
                    price = dig.price2.text()
                    self.total += qun * float(price)
                    dig.label_5.setText(str(self.total))
                    dig.bill.addItem(
                        "{}\t{}\t{} × {} =\t{} ".format(str(qun), prod, str(qun), price, str(qun * float(price))))
                    dig.screen.clear()
                    self.z.append([qun, prod, float(qun) * float(price), billnum])
                    dig.weight.clear()
                    dig.item.clear()
                    dig.price2.clear()

                except Exception as e:
                    print(e)

            def search(self):
                try:
                    conn = sqlite3.connect("m7l.db")
                    c = conn.cursor()
                    dig.textBrowser.show()
                    sender = self.sender().text() + "%"
                    x = sender
                    c.execute("""select * from mobiles where name like (?) or number like (?)""", (x, x))
                    y = c.fetchall()
                    c.close()
                    conn.close()
                    t = ""
                    for i, n in y:
                        t += "{}\t{}\n".format(i, n)
                    dig.textBrowser.setText(t)
                except Exception as e:
                    print(e)

            def createPrinteDialog(self):
                try:
                    bill = ""
                    for i in range(len(dig.bill)):
                        bill += dig.bill.item(i).text() + "\n"
                    printer = QPrinter(QPrinter.ScreenResolution)
                    printer.setPageSize(30)
                    printer.setFullPage(True)
                    painter = QPainter()
                    painter.begin(printer)
                    painter.setFont(QFont("Segoe UI", 10, 1500))
                    painter.drawText(230, 0, 0, 2000, Qt.TextIncludeTrailingSpaces | Qt.AlignRight, bill)
                    painter.end()
                except Exception as e:
                    print(e)

            def removeSel(self):
                try:
                    pric = dig.screen.text()
                    listItems = dig.bill.selectedItems()
                    dig.screen.clear()
                    if not listItems:
                        return

                    if dig.bill.currentRow() not in (0, 1, 2,3):
                        for item in listItems:
                            pric = float(item.text().split("=")[1])
                            self.total -= float(pric)
                            dig.label_5.setText(str(self.total))
                            self.quant = ""
                            dig.bill.takeItem(dig.bill.row(item))
                    else:
                        QMessageBox.information(None, "Error", "لا يمكن الحذف!!!")

                except Exception as e:
                    print(e)

            def addtotable(self):
                try:
                    sender = self.sender().text()
                    x = ""
                    if sender == "دين":
                       if len(dig.bill) <=4:
                           QMessageBox.information(None, "Error", "لا يمكن اضافة فاتورو فارغة!!!")
                       else:
                           dig.customer.clear()
                           dig.mobile.clear()
                           dig.scrollArea_2.show()
                    else:
                        for i in range(dig.bill.count()):
                            if i in (0, 1, 2,3):
                                continue
                            x += dig.bill.item(i).text() + "\n"

                        date = strftime("%Y-%m-%d")
                        time = strftime("%I:%M %p")
                        notes = dig.notes.text()
                        r = dig.tableWidget.rowCount()
                        dig.tableWidget.insertRow(r)
                        dig.tableWidget.setItem(r, 0, QTableWidgetItem(dig.label_4.text()))
                        dig.tableWidget.setItem(r, 1, QTableWidgetItem(x))
                        dig.tableWidget.setItem(r, 2, QTableWidgetItem(str(self.total)))
                        dig.tableWidget.setItem(r, 3, QTableWidgetItem(date))
                        dig.tableWidget.setItem(r, 4, QTableWidgetItem(time))
                        dig.tableWidget.setItem(r, 5, QTableWidgetItem(dig.notes.text()))
                        billnum = dig.label_4.text()


                        conn2 = sqlite3.connect("m7l.db")
                        c2 = conn2.cursor()
                        c2.execute(""" insert into bills (billnum,[date]) values (?,?)""", (dig.label_4.text(), date))
                        conn2.commit()


                        conn = sqlite3.connect("m7l2.db")
                        c = conn.cursor()

                        if sender == ("دفع"):
                            c.execute(
                                """insert into bills (billnum,bill,total,[date],[time],notes,saler) values (?,?,?,?,?,?,?);""",
                                (billnum, x, self.total, date, time, notes, self.saler))
                            conn.commit()
                            dig.bill.addItem("======================================================")
                            dig.bill.addItem("الاجمالي : {} ".format(self.total))
                            dig.bill.addItem("{}\t{}".format(date, time))
                            self.createPrinteDialog()

                        elif sender == "اضافة":
                            customer = dig.customer.text()
                            mobile = dig.mobile.text()
                            c.execute(
                                """insert into dyon (billnum,bill,total,[date],[time],notes,saler,customer,mobile) values (?,?,?,?,?,?,?,?,?);""",
                                (billnum, x, self.total, date, time, notes, self.saler, customer, mobile))
                            conn.commit()
                            dig.scrollArea_2.hide()
                            c2.execute("""select count(*)from mobiles where name =(?) and number =(?)""",(customer,mobile))
                            x=c2.fetchall()[0][0]
                            if x==0 and len(customer)!=0 and len(mobile)!=0:
                                print(customer,mobile)
                                c2.execute("""insert into mobiles (name,number) values (?,?);""",(customer,mobile))
                                conn2.commit()


                        for qun, prod, price, billnum in self.z:
                            c.execute(
                                """insert into sales (quantity,product,price,billnum,[date],[time])values (?,?,?,?,?,?)""",
                                (qun, prod, price, billnum, date, time))
                            conn.commit()
                        c.close()
                        conn.close()
                        c2.close()
                        conn2.close()
                        self.z = []
                        self.total = 0
                        dig.label_5.setText(str(self.total))
                        dig.bill.clear()
                        dig.notes.clear()
                        putter()
                except Exception as e:
                    print(e)

        b = butt()
        def mobiley():
            try:
                mobiles.main()
            except Exception as e:
                print(e)

        def deletefromtable():
            try:
                buttreplay = QMessageBox.question(None, "", " حذف!!!؟؟")
                if buttreplay == QMessageBox.Yes:
                    r = dig.tableWidget.currentRow()
                    billnum = dig.tableWidget.item(r, 0).text()
                    bill = dig.tableWidget.item(r, 1).text()
                    total = dig.tableWidget.item(r, 2).text()
                    date = dig.tableWidget.item(r, 3).text()
                    time = dig.tableWidget.item(r, 4).text()
                    notes = dig.tableWidget.item(r, 5).text()
                    dig.tableWidget.removeRow(r)

                    conn = sqlite3.connect("m7l2.db")
                    c = conn.cursor()
                    c.execute(
                        """DELETE FROm bills where billnum = (?) and bill =(?) and total=(?) and date=(?) and time=(?)""",
                        (billnum, bill, total, date, time))
                    conn.commit()

                    c.execute(
                        """DELETE FROm dyon where billnum = (?) and bill =(?) and total=(?) and date=(?) and time=(?)""",
                        (billnum, bill, total, date, time))
                    conn.commit()

                    c.execute("""delete from sales where billnum=(?) and date=(?) and time=(?)""",
                              (billnum, date, time))
                    conn.commit()
                    c.close()
                    conn.close()
                    putter()
            except Exception as e:
                print(e)

        def eldorg():
            dorg.saler = b.saler
            dorg.stTime = b.stTime
            dorg.main()


        def logout():
            Elmostafa.main()
            dig.hide()

        dig.point.clicked.connect(b.calc)
        dig.multpli.clicked.connect(b.calc)
        dig.zero.clicked.connect(b.calc)
        dig.one.clicked.connect(b.calc)
        dig.two.clicked.connect(b.calc)
        dig.three.clicked.connect(b.calc)
        dig.four.clicked.connect(b.calc)
        dig.five.clicked.connect(b.calc)
        dig.sex.clicked.connect(b.calc)
        dig.seven.clicked.connect(b.calc)
        dig.eight.clicked.connect(b.calc)
        dig.nine.clicked.connect(b.calc)
        dig.clear.clicked.connect(b.calc)
        dig.dele.clicked.connect(b.calc)
        dig.pushButton.clicked.connect(deletefromtable)

        dig.Push_chic.clicked.connect(b.billing)
        dig.push_wrak_2.clicked.connect(b.billing)
        dig.push_feleh_2.clicked.connect(b.billing)
        dig.Push_hyakl_2.clicked.connect(b.billing)
        dig.Push_kbda_2.clicked.connect(b.billing)
        dig.Push_kbdaWoans_2.clicked.connect(b.billing)
        dig.pushButton_3.clicked.connect(b.billing)
        dig.shesh.clicked.connect(b.billing)
        dig.pushButton_5.clicked.connect(b.billing)
        dig.pushButton_6.clicked.connect(b.billing)
        dig.Push_duck.clicked.connect(b.billing)
        dig.Push_dove.clicked.connect(b.billing)
        dig.Push_rabb.clicked.connect(b.billing)
        dig.pushButton_2.clicked.connect(b.billing)
        dig.sdorb3zm.clicked.connect(b.billing)
        dig.additem.clicked.connect(b.additem)
        dig.pushButton_7.clicked.connect(dig.scrollArea.hide)
        dig.comboBox.activated[str].connect(b.combobox)

        dig.pay.clicked.connect(b.addtotable)
        dig.credit.clicked.connect(b.addtotable)
        dig.listdel.clicked.connect(b.removeSel)

        dig.search.textChanged.connect(b.search)
        dig.pushButton_12.clicked.connect(hsabat.main)
        dig.pushButton_13.clicked.connect(mobiley)
        dig.pushButton_16.clicked.connect(prices.main)
        dig.pushButton_14.clicked.connect(wardat.main)
        dig.pushButton_15.clicked.connect(sales.main)
        dig.pushButton_4.clicked.connect(search.main)

        dig.pushButton_9.clicked.connect(eldorg)
        dig.action.triggered.connect(logout)

        dig.addtodatabase.clicked.connect(b.addtotable)
        dig.pushButton_10.clicked.connect(dig.scrollArea_2.hide)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        try:
            close = QMessageBox()
            close.setWindowTitle(" ")
            close.setText("هل تريد الخروج ؟؟؟")
            close.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            close.button(QMessageBox.Yes).setText("نعم")
            close.button(QMessageBox.No).setText("لا")
            close = close.exec()
            Endtime = strftime("%I:%M %p")
            if close == QMessageBox.Yes:
                event.accept()
                total=dorg.select(Endtime)
                dorg.tslem(total,Endtime)
                Elmostafa.app.exit()

            else:
                event.ignore()

        except Exception as e :
            print(e)
            # QMessageBox.information(None, "Error", "a7aaa")


def main(name,id,srTime):
    win = MainWindow(name,id,srTime)
    win.show()


if __name__ == "__main__":
    main("7a",555)
