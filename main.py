import os
import sys
import time
from datetime import datetime
from queue import Queue
from utils import constants
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem, QAbstractItemView, QPushButton, \
    QVBoxLayout
from demo import Ui_Dialog
from libs import Scan, TCPCommunication
from twisted.internet import protocol
from threading import Thread, Lock
from config import config

lock = Lock()

scan = Scan(config.PWD_FOLDER_IMAGE)

queue = Queue()
IS_CLOSE = False


class WCSClient(protocol.Protocol):
    def dataReceived(self, data: bytes) -> None:
        try:
            print(data)
            datas = data.decode().split("|")[:-1]
            for dta in datas:
                queue.put(dta)
        except Exception as e:
            print(e)


tcp_communication = TCPCommunication(config.HOST, config.PORT, WCSClient())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tableWidget.setRowCount(20)
        self.ui.tableWidget.setColumnWidth(0, 185)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.index_table = 0
        self.list_data_in_table = []
        self.setFixedSize(1280, 720)

    def set_table(self, data):
        # lock.acquire()
        try:
            if self.index_table <= 20:
                self.index_table += 1
            else:
                self.list_data_in_table.pop(0)
                for i in range(0, len(self.list_data_in_table)):
                    time.sleep(0.01)
                    self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(self.list_data_in_table[i][0]))
                    self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(self.list_data_in_table[i][1]))

            now = datetime.now()
            print(self.index_table)
            self.ui.tableWidget.setItem(self.index_table - 1, 0,
                                        QTableWidgetItem(now.strftime("%m/%d/%Y %H:%M:%S.%f")[:-4]))
            self.ui.tableWidget.setItem(self.index_table - 1, 1, QTableWidgetItem(data))
            self.list_data_in_table.append([now.strftime("%m/%d/%Y %H:%M:%S.%f")[:-4], data])
            if self.index_table > 10:
                self.ui.tableWidget.scrollToBottom()
        except Exception as e:
            print(e)
        # lock.release()

    def change_image(self, path):
        image = Image.open(path)
        resized_image = image.resize((680, 456), Image.LANCZOS)  # Resize with antialiasing
        resized_image.save(config.PWD_FOLDER_IMAGE + "resize_image.jpg", "JPEG")
        image = QPixmap(config.PWD_FOLDER_IMAGE + "resize_image.jpg")
        resized_image = image.scaled(self.ui.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.label.setPixmap(resized_image)
        os.remove(path=config.PWD_FOLDER_IMAGE + "resize_image.jpg")
        os.remove(path=path)

    def closeEvent(self, a0):
        global IS_CLOSE
        super().closeEvent(a0)
        IS_CLOSE = True
        tcp_communication.close()


def set_table():
    global window, IS_CLOSE
    while not IS_CLOSE:
        try:
            data = queue.get()
            window.set_table(data)
            time.sleep(0.01)
        except Exception as e:
            print(e)


def scan_folder():
    global window, IS_CLOSE
    while not IS_CLOSE:
        image_path = scan.get_last_image()
        if not image_path:
            time.sleep(0.01)
            continue
        window.change_image(image_path)
        time.sleep(0.01)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    thread_set_table = Thread(target=set_table, args=())
    thread_set_table.start()
    thread_scan_folder = Thread(target=scan_folder, args=())
    thread_scan_folder.start()
    os._exit(app.exec_())
