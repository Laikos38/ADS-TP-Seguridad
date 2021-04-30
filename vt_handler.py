from PyQt5.QtCore import QObject, pyqtSignal
import os
import vt
import json
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
        self.progress.emit("Uploading")
        with open(file_path, "rb") as f:
            analysis = self.client.scan_file(f)
        while True:
            analysis = self.client.get_object("/analyses/{}", analysis.id)
            self.progress.emit(analysis.status.capitalize())
            if analysis.status == "completed":
                break
            sleep(3)
        response = self.parse_response(analysis)
        self.finished.emit(response)

    def parse_response(self, analyses):
        resultString = " El archivo fue detectado como inofensivo por " + str(analyses.stats["harmless"]) + " antivirus\n "
        resultString += "Detectado como malicioso por " + str(analyses.stats["malicious"]) + " antivirus\n "
        resultString += "Detectado como sospechoso por " + str(analyses.stats["suspicious"]) + " antivirus\n "
        resultString += "Clasificado como 'No detectado' por " + str(analyses.stats["undetected"]) + " antivirus\n "

        print(resultString)
        return resultString
