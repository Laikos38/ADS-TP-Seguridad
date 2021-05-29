from django.db import models

class VTAnalysis(models.Model):
    date_time_analysis = models.DateTimeField(auto_now_add=True)
    harmless = models.BooleanField(null=True)
    malicious = models.BooleanField(null=True)
    suspicious = models.BooleanField(null=True)
    hash_obj = models.CharField(null=True, max_length=200)
    antiviruses_results = models.TextField(null=True)
    file = models.FileField(null=True, upload_to='uploads/%Y/%m/%d/')

    def get_dict(self):
        return {
            'date_time_analysis': self.date_time_analysis,
            'harmless': self.harmless,
            'malicious': self.malicious,
            'suspicious': self.suspicious,
            'hash_obj': self.hash_obj,
            'antiviruses_results': self.antiviruses_results,
        }

    class Meta:
        db_table = 'vt_analysis'
        indexes = [models.Index(fields=['hash_obj'], name='hash_obj_idx')]
        ordering = ['-date_time_analysis']
