from gui.gui import *
from platform import platform
from functools import partial
from vt_handler import VtHandler
import re
import os


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        # Cargar GUI
        self.setupUi(self)

        # Determinar OS
        self.determine_os()
        
        # QMessageBox
        self.msg_box = QtWidgets.QMessageBox

        # Virus Total Handler
        try:
            self.vt_handler = VtHandler()
        except ValueError:
            self.msg_box.critical(self, 'Error', 'No se detectó una API Key válida de Virus Total.')
            os._exit(1)

        # Thread
        self.thread = QtCore.QThread()
        self.worker = self.vt_handler
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.vt_handler.scan_file, ""))
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.thread.quit)

        # Ocultar items
        self.uploadPb.setVisible(False)
        self.checkHarmlessLbl.setVisible(False)
        self.crossHarmlessLbl.setVisible(False)
        self.checkMaliciousLbl.setVisible(False)
        self.crossMaliciousLbl.setVisible(False)
        self.checkSuspiciousLbl.setVisible(False)
        self.crossSuspiciousLbl.setVisible(False)
        self.uploadBtn.clicked.connect(self.open_file_dialog)

    def determine_os(self):
        so = platform()
        if re.search("linux", so, re.IGNORECASE):
            self.os = 'linux'
        elif re.search("windows", so, re.IGNORECASE):
            self.os = 'windows'
        elif re.search("darwin", so, re.IGNORECASE):
            self.os = 'darwin'
        else:
            self.os = 'ukn'

    def open_file_dialog(self):
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if self.os == 'windows':
            fileDialog.setNameFilter("*.exe")
        if fileDialog.exec_():
            filename = fileDialog.selectedFiles()[0]
            if self.os == 'linux' or self.os == 'darwin':
                if not is_exe(filename[0]):
                    self.msg_box.critical(self, 'Error', "Esto no es un ejecutable.")
                    return
            self.clear_thread_connections()
            self.thread.started.connect(partial(self.vt_handler.scan_file, filename))
            self.thread.start()

    def block_gui(self):
        self.uploadBtn.setEnabled(False)
        self.uploadPb.setVisible(True)

    def unblock_gui(self):
        self.uploadBtn.setEnabled(True)
        self.uploadPb.setVisible(False)

    def update_progress(self, msg):
        self.statusbar.showMessage(msg)

    def show_response(self, responseDict):
        self.resultsTe.setPlainText(responseDict['full_results'])
        if responseDict['resume_stats']['harmless'] <= 0:
            self.checkHarmlessLbl.setVisible(True)
        else:
            self.crossHarmlessLbl.setVisible(True)
        if responseDict['resume_stats']['malicious'] <= 0:
            self.checkMaliciousLbl.setVisible(True)
        else:
            self.crossMaliciousLbl.setVisible(True)
        if responseDict['resume_stats']['suspicious'] <= 0:
            self.checkSuspiciousLbl.setVisible(True)
        else:
            self.crossSuspiciousLbl.setVisible(True)
        self.tabWidget.setCurrentIndex(1)

    def clear_thread_connections(self):
        self.thread.started.disconnect()
        self.worker.progress.disconnect()
        self.worker.finished.disconnect()
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.unblock_gui)
        self.worker.finished.connect(self.show_response)
        self.worker.progress.connect(self.update_progress)
        self.worker.started.connect(self.block_gui)


def is_exe(fpath):
    return os.access(fpath, os.X_OK)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()