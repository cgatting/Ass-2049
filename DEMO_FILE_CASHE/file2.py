from PyQt5.QtWidgets import QApplication, QWidget

class File2Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.showMaximized()
        self.setWindowTitle('File 2 Window')

if __name__ == '__main__':
    app = QApplication([])
    ex = File2Window()
    ex.show()
    app.exec_()
