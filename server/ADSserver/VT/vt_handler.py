from django.conf import settings
from time import sleep
import vt

class VtAPIKeyError(Exception):
    pass

class VtHandler():
    def __init__(self):
        super().__init__()
        self.apikey = settings.VT_API_KEY
        if self.apikey is None:
            raise VtAPIKeyError
        self.client = vt.Client(self.apikey)
    
    def scan_file(self, file_path):
        response = None
        with open(file_path, "rb") as f:
            analysis = self.client.scan_file(f)
            while True:
                analysis = self.client.get_object("/analyses/{}", analysis.id)
                if analysis.status == "completed":
                    break
                # sleep(3)
            response = self.parse_response(analysis)
        return response

    def parse_response(self, analyses):
        stats = {
            'harmless': analyses.stats["harmless"] <= 0 ,
            'malicious': analyses.stats["malicious"] <= 0,
            'suspicious': analyses.stats["suspicious"] <= 0
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