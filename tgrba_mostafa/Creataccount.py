from PyQt5 import QtWidgets, uic

from PyQt5.QtWidgets import *

import sqlite3
        # """ Connecting to database"""


            # """ Defining th ui file"""
app = QtWidgets.QApplication([])
dig = uic.loadUi("creat.ui")

def main():

    def creat():
        try:
            username= dig.lineEdit.text()
            password= dig.lineEdit_2.text()
            if len(password) ==0 :
                QMessageBox.information(None, "Error!", "ادخل كلمة السر !!!!")
            elif  len(username)==0:
                QMessageBox.information(None, "Error!", "ادخل اسم المستخدم !!!!")
            else:
                conn = sqlite3.connect("m7l2.db")
                c = conn.cursor()
                c.execute("""INSERT INTO stuff(username,password) VALUES(?,?) """,(username,password))
                conn.commit()
                c.close()
                conn.close()
                QMessageBox.information(None,"Succesful","تم عمل اكونت بنجاح")

        except Exception as e :
            print("Creataccount")
            print(e)
            QMessageBox.information(None,"Error!","خطأ جرب اسم اخر اخر !")
        finally:
            dig.lineEdit.clear()
            dig.lineEdit_2.clear()

    dig.pushButton.clicked.connect(creat)
    dig.lineEdit_2.returnPressed.connect(creat)
    dig.show()
    app.exec()

if __name__ == '__main__':
    main()