import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from file2 import File2Window

class File1Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle('File 1 Window')

        open_file2_button = QPushButton('Open File 2', self)
        open_file2_button.clicked.connect(self.open_file2)

    def open_file2(self):
        self.file2_window = File2Window()
        self.file2_window.show()
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = File1Window()
    ex.show()
    sys.exit(app.exec_())
