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
        self.apikey = os.getenv('VT_API_KEY')
        if self.apikey is None:
            raise ValueError
        self.client = vt.Client(self.apikey)
    
    def scan_file(self, file_path):
        self.started.emit(None)
        self.progress.emit("Uploading")
        self.client = vt.Client(self.apikey)
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
        stats = {
            'harmless': analyses.stats["harmless"],
            'malicious': analyses.stats["malicious"],
            'suspicious': analyses.stats["suspicious"]
        }
         
        resultsDict = analyses.to_dict()['attributes']['results']
        resultStr = ""
        for k, v in resultsDict.items():
            resultStr += "Antivirus " + k + ": " + v['category'] + ".\n"
        response = {
            "resume_stats": stats,
            "full_results": resultStr
        }

        return response
