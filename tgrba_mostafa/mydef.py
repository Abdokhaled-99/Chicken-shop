from PyQt5 import QtWidgets, uic
import Elmostafa
import sys
from PyQt5.QtWidgets import *
from uuid import getnode as get_mac




# app = QtWidgets.QApplication([])
dig= uic.loadUi("defenition.ui")


def defualt (n,w):
    with open("mine.txt") as f:
            d = f.readlines()
    with open("mine.txt", "w") as f:
        if n == 0 :
            f.writelines([d[n],w])
        else:
            f.writelines([w,d[n]])
    Elmostafa.main2()
def check():
    x = dig.lineEdit.text()
    if x == "012a420b69d49o":
        defualt(0,"ok")
    elif x == "mac012a420b69d49o" :
        defualt(1,str(get_mac())+"\n")

    else:
        QMessageBox.information(None, "تحذير !!!", "يرجى التواصل مع مطور البرنامج !!")



dig.lineEdit.returnPressed.connect(check)

def main():
    dig.show()
    # app.exec()


if __name__ == '__main__':
    main()
