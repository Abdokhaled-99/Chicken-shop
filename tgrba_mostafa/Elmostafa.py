from PyQt5 import QtWidgets, uic

from PyQt5.QtWidgets import *
import sqlite3
import Creataccount,mydef,grb

import datetime
from uuid import getnode as get_mac
from time import gmtime,strftime



#         # """ Connecting to database"""
# conn = sqlite3.connect("m7l2.db")
# c = conn.cursor()
#             # """ Creating table for stuff"""
# c.execute(""" CREATE TABLE IF NOT EXISTS stuff(Username text,Password text )""")
# conn.commit()
# c.close()
# conn.close()
            # """ Defining th ui file"""
app = QtWidgets.QApplication([])
dig = uic.loadUi("Login.ui")



            # """ make login butt disabled"""



dig.pushButton.setDisabled(True)
def disableButton ():
    if len(dig.lineEdit.text())> 0 :
        dig.pushButton.setDisabled(False)
    else:
        dig.pushButton.setDisabled(True)
dig.lineEdit.textChanged.connect(disableButton)

            # """ make password visible and invisible"""
def state ():
    if dig.checkBox.isChecked():
        dig.lineEdit_2.setEchoMode(QLineEdit.Normal)
    else:
        dig.lineEdit_2.setEchoMode(QLineEdit.Password)

dig.checkBox.stateChanged.connect(state)

        #""" checking of user name and password"""
def loging():
    try:
        conn = sqlite3.connect("m7l2.db")
        c = conn.cursor()
        Username = (dig.lineEdit.text(),)
        Password = dig.lineEdit_2.text()
        c.execute("""select Password ,salerid from stuff where Username = (?)""",(Username))
        result = c.fetchone()
        c.close()
        conn.close()
        if result[0] == Password:
           conn2 = sqlite3.connect("m7l.db")
           c2 = conn2.cursor()
           grb.main(Username[0],result[1],strftime("%I:%M %p"))
           c2.execute("""insert into dorg (saler,stTime,Entime,total,date) values (?,?,?,?,?);""",(Username[0],strftime("%I:%M %p"),strftime("%I:%M %p"),0.0,strftime("%Y-%m-%d")))
           conn2.commit()
           c2.close()
           conn2.close()
           dig.hide()

        else:
            QMessageBox.information(None,"Error!","User name or password is wrong")
    except Exception as e :
        if type(e) == TypeError:
            QMessageBox.information(None, "Error", "هذا الحساب غير موجود !!!")
        print("Elmostafa,loging")
        print(e)




dig.pushButton.clicked.connect(loging)
dig.lineEdit_2.returnPressed.connect(loging)
dig.pushButton_2.clicked.connect(Creataccount.main)

def main():
    dig.lineEdit.clear()
    dig.lineEdit_2.clear()
    dig.show()
def main2():
    with open("mine.txt") as f:
        data = f.readlines()
    if get_mac() != int(data[0]) or (datetime.date.today() > datetime.date(2019, 4,18) and data[1] != "ok"):
        mydef.main()
    else:
        main()

if __name__ == '__main__':
    main()
    app.exec()
