import os
import sys
import csv
import time
import json
import threading
from locale import setlocale, atof, LC_ALL

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QTabWidget, QWidget, QVBoxLayout,
                             QTableWidget, QAbstractItemView, QAbstractScrollArea, QDialog, QLabel, QDesktopWidget)

from crypto import Crypto, Wallet


class Loading(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setFixedSize(300, 100)
        self.center()
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        vbox = QVBoxLayout()
        self.lbl = QLabel("Initializing wallet.")
        self.lbl.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.lbl)
        self.setLayout(vbox)
        self.show()

        self.allowed_to_close = False

        thread = threading.Thread(target=self.loop_text)
        thread.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loop_text(self):
        while not self.allowed_to_close:
            time.sleep(1)
            if str(self.lbl.text()).count('.') == 1:
                self.lbl.setText("Initializing wallet..")
            elif str(self.lbl.text()).count('.') == 2:
                self.lbl.setText("Initializing wallet...")
            elif str(self.lbl.text()).count('.') == 3:
                self.lbl.setText("Initializing wallet.")

    def closeEvent(self, evnt):
        if self.allowed_to_close:
            super().closeEvent(evnt)
        else:
            evnt.ignore()


class Window(QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Personal Crypto Tracker")
        self.setGeometry(50, 50, 600, 400)

        # TODO: progress bar
        self.init_loading()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1, "Crypto Wallet")
        self.addTab(self.tab2, "Fiat Deposits and Withdrawal")
        self.addTab(self.tab3, "Trade History")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        self.show()

    def init_loading(self):
        self.dialog = Loading()

        thread = threading.Thread(target=self.read_wallet_thread)
        thread.start()

    def tab1UI(self):
        vbox = QVBoxLayout()

        self.tab1.setLayout(vbox)

    def tab2UI(self):
        vbox = QVBoxLayout()
        table = QTableWidget(5, 3)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.resizeColumnsToContents()
        table.setHorizontalHeaderLabels(["Date", "Amount", "Currency"])
        vbox.addWidget(table)

        self.tab2.setLayout(vbox)

    def tab3UI(self):
        vbox = QVBoxLayout()

        self.tab3.setLayout(vbox)

    def read_wallet_thread(self):
        self.w = Wallet()
        self.read_crypto_file("crypto/crypto.csv")
        self.read_deposits_file("crypto/deposits.csv")
        print("Done")
        self.dialog.allowed_to_close = True
        self.dialog.close()

    def read_crypto_file(self, file_name):
        """
        Read crypto.csv and returns a list of crypto objects
        """
        print("Loading crypto...")

        try:
            with open(file_name, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",", quotechar="|")
                next(csv_reader, None)  # Skip header
                for row in csv_reader:
                    self.w.add_coin(Crypto(row[0], row[1], atof(row[2])))
        except IOError:
            raise Exception("Err#100: CSV file for crypto not found.")
        except Exception as e:
            raise Exception(f"{e}\nErr#109: Something went terribly wrong.")

    def read_deposits_file(self, file_name):
        """
        Read deposits.csv and returns a list deposits in dict
        """
        print("Loading deposits...")

        try:
            with open(file_name, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                next(csv_reader, None)  # Skip header
                for row in csv_reader:
                    self.w.add_deposit({"Date": row[0],
                                        "Amount": atof(row[1]),
                                        "Currency": row[2]})
        except IOError:
            raise Exception("Err#110: CSV file for crypto not found.")
        except Exception as e:
            raise Exception(f"{e}\nErr#119: Something went terribly wrong.")


def main():
    try:
        setlocale(LC_ALL, "en_US.utf8")
    except Exception:
        try:
            setlocale(LC_ALL, "en_US.UTF-8")
        except Exception as e:
            raise Exception(f"{e}\nErr#000: locale error.")

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
