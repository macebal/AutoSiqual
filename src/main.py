import logging
import pyautogui
import sys
from gui.about import Ui_About
from gui.log import Ui_LogWindow
from gui.main import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from src import CONFIG, __version__
from src.autosiqual import start_robot
from sys import exit


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setFixedSize(QtCore.QSize(275, 160))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"AutoSiqual - v{__version__}")
        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint  # The first 3 flags are for the window to be on top of everything.
            | QtCore.Qt.WindowStaysOnTopHint
        )

        # parse config file
        self.config = CONFIG
        if self.config is None:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                "Ocurrió un problema al tratar de leer la configuración",
                QtWidgets.QMessageBox.Ok,
            )
            exit(1)

        self.populate_fields()

        self.ui.btn_start.clicked.connect(self.input_data)
        self.ui.actn_help.triggered.connect(self.open_about_wndw)
        self.ui.actn_exit.triggered.connect(self.exit_app)
        self.ui.chckbxDisplayLog.toggled.connect(self.toggle_log)

        # initialize custom logger
        self.log = LogWindow(self)
        self.logger = logging.getLogger("ui_logger")
        self.logger.addHandler(self.log)
        self.logger.setLevel(logging.INFO)

        self.log.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))

    def populate_fields(self):
        try:
            active_plant = self.config.active_plant
            products = active_plant.materials.get_product_names()
            raw_materials = active_plant.materials.get_raw_material_names()

            self.ui.le_plant.setText(active_plant.name)

            self.ui.cb_product.addItems(products)
            self.ui.cb_product.addItem("") if len(products) > 0 and len(raw_materials) > 0 else None
            self.ui.cb_product.addItems(raw_materials)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)
            exit(1)

    def input_data(self):
        self.log.clear_log()
        material = str(self.ui.cb_product.currentText())

        if len(material) > 0:
            w, h = pyautogui.size()  # size of screen

            self.move(
                w - self.size().width() - 25, h - self.size().height() - 75
            )  # move the window to the bottom right corner
            self.log.move(
                self.pos().x() - self.log.size().width() - 2, self.pos().y()
            )  # add the log window to the left of it

            if self.ui.chckbxDisplayLog.isChecked():
                self.log.show()

            self.logger.info(f"********  AutoSiqual v{__version__}  ********")

            try:
                start_robot(material)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e), QtWidgets.QMessageBox.Ok)
                print(e.with_traceback())
                exit(1)

        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Advertencia",
                "Seleccione un material válido.",
                QtWidgets.QMessageBox.Ok,
            )

    def open_about_wndw(self):
        about = QtWidgets.QDialog()
        about.ui = Ui_About()
        about.ui.setupUi(about)
        about.ui.label_2.setText(__version__)
        about.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint  # The first 3 flags are for the window to be on top of everything.
            | QtCore.Qt.WindowStaysOnTopHint
        )
        about.exec_()
        about.show()

    def exit_app(self):
        exit(0)

    def toggle_log(self):
        if self.ui.chckbxDisplayLog.isChecked():
            self.log.show()
        else:
            self.log.hide()


class LogWindow(QtWidgets.QMainWindow, logging.Handler):
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.ui = Ui_LogWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("AutoSiqual - Log")

        self.edit = self.ui.log_text_edit  # the componenct that I'll log into

    def emit(self, record):
        # this method has to be implemented fo the logger to emit in this component
        self.edit.appendPlainText(self.format(record))

    def clear_log(self):
        self.edit.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())
