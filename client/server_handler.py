from PyQt5.QtCore import QObject, pyqtSignal
import os
from aiohttp.client import request
from requests.sessions import Request
import vt
from time import sleep
import requests
import hashlib

class ServerHandler(QObject):
    started = pyqtSignal(object)
    finished = pyqtSignal(object)
    progress = pyqtSignal(object)
    server_URL = 'http://127.0.0.1:8000/analysis/'
    checkHash_URL = server_URL+'get-by-hash/'
    uploadFile_URL = server_URL+'upload/'

    def get_analysis(self, filePath):
        self.started.emit(None)
        self.progress.emit("Uploading")
        hash = md5(filePath)
        hash_result = self.check_for_analysis_hash(hash)

        if hash_result is None:
            upload_result = self.upload_file(filePath)     
            print(upload_result)           
            self.finished.emit(upload_result)
        else: 
            self.finished.emit(hash_result)

    def check_for_analysis_hash(self, hash):
        response = requests.get(self.checkHash_URL+hash)
        if response.status_code == requests.codes.ok:
            response = response.json()
            if response['analysis'] is None:
                return None
            else:
                return response
        return 'Error'

    def upload_file(self, filePath):
        file = {'file': open(filePath, 'rb')}
        response = requests.post(self.uploadFile_URL, files=file)

        if response.status_code == requests.codes.ok:
            response = response.json()
            return response
        return 'Error'
    
def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()                         