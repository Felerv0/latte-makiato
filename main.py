import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic, Qt


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Капучино')
        uic.loadUi('main.ui', self)

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.btn.clicked.connect(self.loadTable)
        self.btn_edit.clicked.connect(self.editWindow)

    def loadTable(self):
        res = self.cur.execute("""SELECT coffees.id, coffees.name, roast.level, coffees.taste,
        seed.title, coffees.cost, coffees.volume
        FROM coffees INNER JOIN roast ON coffees.roast_level = roast.id 
        INNER JOIN seed ON coffees.seeds = seed.id""").fetchall()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Обжарка', 'Вкус', 'Вид', 'Стоимость, руб', 'Объём, г'])
        self.table.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, s in enumerate(elem):
                item = QTableWidgetItem(str(s))
                item.setFlags(Qt.Qt.ItemIsSelectable | Qt.Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)

    def editWindow(self):
        self.edit = Edit()
        self.edit.show()


class Edit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Редактирование')
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        roast = self.cur.execute("""SELECT level FROM roast""").fetchall()
        seed = self.cur.execute("""SELECT title FROM seed""").fetchall()
        for i in range(len(roast)):
            self.roast.addItem(roast[i][0])
        for i in range(len(seed)):
            self.type.addItem(seed[i][0])

        self.load_btn.clicked.connect(self.loadByID)
        self.save_btn.clicked.connect(self.saveCoffee)

    def loadByID(self):
        self.err.setText('')
        current_id = self.id_inp.value()
        res = self.cur.execute("""SELECT * FROM coffees WHERE id = ?""", (current_id,)).fetchall()
        if len(res) == 0:
            self.err.setText('Нет такого ID')
        else:
            self.name.setText(res[0][1])
            self.roast.setCurrentIndex(res[0][2] - 1)
            self.type.setCurrentIndex(res[0][3] - 1)
            self.taste.setText(res[0][4])
            self.cost.setValue(res[0][5])
            self.volume.setValue(res[0][6])

    def saveCoffee(self):
        self.err.setText('')
        ids = [i[0] for i in self.cur.execute("""SELECT id FROM coffees""").fetchall()]
        if self.id_inp.value() in ids:
            self.cur.execute("""UPDATE coffees SET name = ?, roast_level = ?, seeds = ?, 
                    taste = ?, cost = ?, volume = ? WHERE id = ?""",
                             (self.name.text(), self.roast.currentIndex() + 1, self.type.currentIndex() + 1,
                              self.taste.text(), self.cost.value(), self.volume.value(), self.id_inp.value()))
        else:
            self.cur.execute("""INSERT INTO coffees VALUES(?, ?, ?, ?, ?, ?, ?)""",
                             (self.id_inp.value(), self.name.text(), self.roast.currentIndex() + 1,
                              self.type.currentIndex() + 1, self.taste.text(), self.cost.value(), self.volume.value()))
        self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Espresso()
    gui.show()
    sys.exit(app.exec_())