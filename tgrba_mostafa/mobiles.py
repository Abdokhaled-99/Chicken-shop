from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sqlite3
dig= uic.loadUi("mobiles.ui")
dig.pushButton.setDisabled(True)
dig.pushButton_2.setDisabled(True)
dig.pushButton_3.setDisabled(True)
# dig.pushButton_4.setDisabled(True)
def disableButton ():
    if len(dig.lineEdit.text())> 0 or len(dig.lineEdit_2.text())> 0 :
        dig.pushButton.setDisabled(False)
        dig.pushButton_2.setDisabled(False)
        dig.pushButton_3.setDisabled(False)
        # dig.pushButton_4.setDisabled(False)
    else:
        dig.pushButton.setDisabled(True)
        dig.pushButton_2.setDisabled(True)
        dig.pushButton_3.setDisabled(True)
        # dig.pushButton_4.setDisabled(True)
dig.lineEdit.textChanged.connect(disableButton)
dig.lineEdit_2.textChanged.connect(disableButton)

def searchy():
    try:
        dig.tableWidget.setRowCount(0)
        flag=dig.lineEdit.text()
        flag2=dig.lineEdit_2.text()
        conn = sqlite3.connect("m7l.db")
        c=conn.cursor()
        if len(dig.lineEdit.text())>0 and len(dig.lineEdit_2.text())>0:
            c.execute("""select * from mobiles where name = (?)  and number = (?)""",(flag,flag2))

        else:
            c.execute("""select * from mobiles where (?) in(name,number) or (?) in (name,number) """,(flag,flag2))
        for i , n in c.fetchall():
            r= dig.tableWidget.rowCount()
            dig.tableWidget.insertRow(r)
            dig.tableWidget.setItem(r,0,QTableWidgetItem(i))
            dig.tableWidget.setItem(r,1,QTableWidgetItem(n))
    except Exception as e:
        QMessageBox.information(None, "Error!","Error!!")
class butt(QPushButton):
    def updately(self):
        try:
            name=dig.lineEdit.text()
            number=dig.lineEdit_2.text()
            conn=sqlite3.connect("m7l.db")
            c=conn.cursor()
            if self.sender().text() == "تحديث":
                r = dig.tableWidget.currentRow()
                field1 = dig.tableWidget.item(r, 0).text()
                field2 = dig.tableWidget.item(r, 1).text()
                c.execute("""update mobiles set number =(?)  where name =(?) and number =(?)  ;""",(number,field1,field2))
                conn.commit()
                searchy()
            elif self.sender().text() == "اضافة":
                c.execute("""insert into mobiles (name,number) values (?,?)""",(name,number))
                conn.commit()
                searchy()
            elif self.sender().text() == "حذف":
                buttreplay = QMessageBox.question(None, "", " حذف!!!؟؟")
                if buttreplay == QMessageBox.Yes:

                    r=dig.tableWidget.currentRow()
                    field1=dig.tableWidget.item(r,0).text()
                    field2=dig.tableWidget.item(r,1).text()
                    dig.tableWidget.removeRow(r)
                    c.execute("""DELETE FROm mobiles where name =(?) and number = (?)""",(field1,field2))
                    conn.commit()
            c.close()
            conn.close()
        except Exception as e:
            if type(e) == sqlite3.IntegrityError:
                QMessageBox.information(None, "Error", "هذا الرقم موجود من قبل!!!!")
            print(type(e))

def onOPen():
    conn = sqlite3.connect("m7l.db")
    c = conn.cursor()
    c.execute("""select * from mobiles""")
    dig.tableWidget.setRowCount(0)
    for i, n in c.fetchall():
        r = dig.tableWidget.rowCount()
        dig.tableWidget.insertRow(r)
        dig.tableWidget.setItem(r, 0, QTableWidgetItem(i))
        dig.tableWidget.setItem(r, 1, QTableWidgetItem(n))
    c.close()
    conn.close()
b=butt()

dig.pushButton_4.clicked.connect(b.updately)
dig.pushButton_2.clicked.connect(searchy)
dig.pushButton_3.clicked.connect(b.updately)
dig.pushButton.clicked.connect(b.updately)
def main():
    onOPen()
    dig.show()
if __name__ == '__main__':
    main()