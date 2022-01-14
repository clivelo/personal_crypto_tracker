import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout


class Window(QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Personal Crypto Tracker")
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1, "Dashboard")
        self.addTab(self.tab2, "Crypto")
        self.addTab(self.tab3, "History")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    def tab1UI(self):
        pass

    def tab2UI(self):
        pass

    def tab3UI(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
