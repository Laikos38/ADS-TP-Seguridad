from gui.gui import *
from platform import platform
import os


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.determine_os()

        # QMessageBox
        self.msg_box = QtWidgets.QMessageBox

        self.uploadPb.setVisible(False)
        self.uploadBtn.clicked.connect(self.open_file_dialog)

    def determine_os(self):
        so = platform()
        if 'linux' in so:
            self.os = 'linux'
        elif 'windows' in so:
            self.os = 'windows'
        elif 'darwin' in so:
            self.os = 'darwin'
        else:
            self.os = 'ukn'

    def open_file_dialog(self):
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if self.os == 'windows':
            fileDialog.setNameFilter("*.exe")
        if fileDialog.exec_():
            filenames = fileDialog.selectedFiles()
            if self.os == 'linux' or self.os == 'darwin':
                if not is_exe(filenames[0]):
                    self.msg_box.critical(self, 'Error', "Esto no es un ejecutable.")

            print(filenames)


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()