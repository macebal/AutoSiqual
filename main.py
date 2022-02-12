# AutoSiqual
# v2.0.0
# Mariano Acebal
# 2021

# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.py"
# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.py"
# pyinstaller main.py --onefile

from datetime import datetime
from distutils.command.config import config
import json
import logging, sys
from pprint import pprint
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from matplotlib.font_manager import json_dump
import pyautogui
from PasteData import paste_data
from config import ConfigParser
from gui import Ui_MainWindow  # importing the ui
from log import Ui_LogWindow
from AutoSiqual import start_robot
from excel_parser import ParserFactory

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(mainWindow, self).__init__()
        self.setFixedSize(QSize(275, 150))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("AutoSiqual - v2.0.0")
        self.setWindowFlags(
        QtCore.Qt.Window |
        QtCore.Qt.CustomizeWindowHint |
        QtCore.Qt.WindowTitleHint | # The first 3 flags are for the window to be on top of everything.
        QtCore.Qt.WindowCloseButtonHint |
        QtCore.Qt.WindowStaysOnTopHint
        )

        #parse config file
        try:
            self.config = ConfigParser()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)
            exit(1)

        self.populate_fields()

        #Testing
        # plant_code, _ = self.config.get_active_plant_names()
        # test_date = datetime(2022,1,4)
        # factory = ParserFactory.ParserFactory()
        # parser = factory.getParser(plant_code)
        # data = parser.parse_materials(test_date, "Clinker")
        # print(data)
        # paste_data(data,"CPC30")
        
        # json_dump(data, 'C:\\Users\\macebal\\Desktop\\Python\\AutoSiqual\\dump.json')
        # exit(0)
        self.ui.btn_start.clicked.connect(self.inputData)
        
        #initialize custom logger
        self.log = LogWindow(self)
        self.logger = logging.getLogger('ui_logger')
        self.logger.addHandler(self.log)
        self.logger.setLevel(logging.INFO)

        self.log.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%H:%M:%S"))

    def populate_fields(self):
        try:
            _ , active_plant_name = self.config.get_active_plant_names()
            products, raw_materials = self.config.get_materials()

            self.ui.le_plant.setText(active_plant_name)

            self.ui.cb_product.addItems(products)
            self.ui.cb_product.addItem("") if len(products) > 0 and len(raw_materials) > 0 else None
            self.ui.cb_product.addItems(raw_materials)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)
            exit(1)

    def inputData(self):
        self.log.clear_log()
        material = str(self.ui.cb_product.currentText())
        
        if len(material) > 0:
            w, h = pyautogui.size() #size of screen

            self.move(w - self.size().width() - 25,h - self.size().height() - 75) # move the window to the bottom right corner
            self.log.move(self.pos().x() - self.log.size().width() - 2, self.pos().y()) #add the log window to the left of it
            self.log.show()

            self.logger.info("********  AutoSiqual V2.0.0  ********")
            
        try:
            # start_robot(material)
            pass
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)
            exit(1)
            
        else:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione un material válido.", QtWidgets.QMessageBox.Ok)

class LogWindow(QtWidgets.QMainWindow, logging.Handler):
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.ui = Ui_LogWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("AutoSiqual - Log")
        
        self.edit = self.ui.log_text_edit #the componenct that I'll log into

    def emit(self, record):
        #this method has to be implemented fo the logger to emit in this component
        self.edit.appendPlainText(self.format(record)) 
        
    def clear_log(self):
        self.edit.clear()

app = QtWidgets.QApplication([])

application = mainWindow()

application.show()

sys.exit(app.exec())