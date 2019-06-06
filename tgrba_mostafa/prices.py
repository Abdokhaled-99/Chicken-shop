from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sqlite3
app = QtWidgets.QApplication([])
dig= uic.loadUi("prices.ui")


def save():
    try:
        conn = sqlite3.connect("m7l.db")
        c = conn.cursor()
        c.execute("""UPDATE meneu
       SET price = CASE product 
                          WHEN 'فراخ بيضاء' THEN (?) 
                          WHEN 'عتاقي' THEN (?) 
                          WHEN 'شمورت' THEN (?) 
                          WHEN 'حمام' THEN (?) 
                          WHEN 'اوز' THEN (?) 
                          WHEN 'بط' THEN (?) 
                          WHEN 'ارانب' THEN (?) 
                          WHEN 'دبابيس' THEN (?) 
                          WHEN 'وراك' THEN (?) 
                          WHEN 'شيش' THEN (?) 
                          WHEN 'شاورما' THEN (?) 
                          WHEN 'اجنحة' THEN (?) 
                          WHEN 'كبدوقوانص' THEN (?) 
                          WHEN 'كبده' THEN (?) 
                          WHEN 'بانيه' THEN (?) 
                          WHEN 'هياكل' THEN (?) 
                          WHEN 'صدور بعظم' THEN (?) 
                          ELSE price
                          END
     WHERE product IN
    ("فراخ بيضاء","بط","شمورت","عتاقي","حمام","ارانب","اوز","دبابيس","وراك","شيش","شاورما","اجنحة","كبدوقوانص","كبده","بانيه","هياكل","صدور بعظم") 
     
     """,(dig.chick.text(),dig.ata2i.text(),dig.shmort.text(),dig.dove.text(),dig.wez.text(),dig.duck.text(),dig.rabb.text(),dig.dabos.text(),dig.wrak.text(),
        dig.shesh.text(),dig.shawrma.text(),dig.agn7a.text(),dig.kbdw2wans.text(),dig.kbda.text(),dig.baneh.text(),dig.hyakl.text(),dig.sdorb3zm.text()))
        conn.commit()
        c.close()
        conn.close()
    except Exception as e :
        print(e)

def putters():
    conn = sqlite3.connect("m7l.db")
    c = conn.cursor()
    x={"فراخ بيضاء":dig.chick,"بط":dig.duck,"عتاقي":dig.ata2i,"شمورط":dig.shmort,"حمام":dig.dove,"اوز":dig.wez,
       "ارانب":dig.rabb,"دبابيس":dig.dabos,"هياكل":dig.hyakl,"وراك":dig.wrak,"بانيه":dig.baneh,"شيش":dig.shesh,"شاورما":dig.shawrma,"اجنحة":dig.agn7a,"كبده":dig.kbda,
       "كبدوقوانص":dig.kbdw2wans,"صدور بعظم":dig.sdorb3zm}
    c.execute("select product,price from meneu")
    for i,n  in c.fetchall():
        x[i].setText(n)
    c.close()
    conn.close()

putters()
def main():
    dig.pushButton.clicked.connect(save)
    dig.show()
    app.exec_()

if __name__ == '__main__':
    main()