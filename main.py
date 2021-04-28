from gui.gui import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.uploadPb.setVisible(False)

        self.uploadBtn.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        fileDialog.setNameFilter("*.exe")
        if fileDialog.exec_():
            filenames = fileDialog.selectedFiles()
            print(filenames)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()