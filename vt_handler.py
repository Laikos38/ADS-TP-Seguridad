from PyQt5.QtCore import QObject, pyqtSignal
import os
import vt
from time import sleep


class VtHandler(QObject):
    started = pyqtSignal(object)
    finished = pyqtSignal(object)
    progress = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        apikey = os.getenv('VT_API_KEY')
        if apikey is None:
            raise ValueError
        self.client = vt.Client(apikey)
    
    def scan_file(self, file_path):
        self.started.emit(None)
        for i in range(0, 4):
            sleep(1)
            self.progress.emit(i)
        self.finished.emit(None)
