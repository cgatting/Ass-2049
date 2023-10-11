import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class InputPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.input_text = QLineEdit(self)
        self.next_button = QPushButton("Next", self)

        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.next_button)
        self.setLayout(self.layout)

        self.next_button.clicked.connect(self.showNextPage)

    def showNextPage(self):
        input_text = self.input_text.text()
        self.next_page = DisplayPage(input_text)
        self.next_page.show()
        self.close()

class DisplayPage(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.display_label = QLabel("You entered:")
        self.display_text = QLabel(self.text)

        self.layout.addWidget(self.display_label)
        self.layout.addWidget(self.display_text)
        self.setLayout(self.layout)

def main():
    app = QApplication(sys.argv)
    input_page = InputPage()
    input_page.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
