import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic, Qt


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.btn.clicked.connect(self.loadTable)

    def loadTable(self):
        res = self.cur.execute("""SELECT coffees.name, roast.level, coffees.taste,
        seed.title, coffees.cost, coffees.volume
        FROM coffees INNER JOIN roast ON coffees.roast_level = roast.id 
        INNER JOIN seed ON coffees.seeds = seed.id""").fetchall()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Название', 'Обжарка', 'Вкус', 'Вид', 'Стоимость', 'Объём'])
        self.table.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, s in enumerate(elem):
                item = QTableWidgetItem(str(s))
                item.setFlags(Qt.Qt.ItemIsSelectable | Qt.Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Espresso()
    gui.show()
    sys.exit(app.exec_())