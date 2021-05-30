from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
import hashlib
from .models import VTAnalysis
from .vt_handler import VtAPIKeyError, VtHandler


def get_analysis_by_hash(request, hash_obj):
    if request.method != 'GET':
        return HttpResponseBadRequest("Método incorrecto.")
    if not hash_obj:
        return HttpResponseBadRequest("Faltan datos necesarios.")
    analysis = None
    analysis = VTAnalysis.objects.filter(hash_obj=hash_obj).first()
    if analysis is not None:
        analysis = analysis.get_dict()
    return JsonResponse({'analysis': analysis})


def upload_file(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Método incorrecto.")
    if len(request.FILES) < 1:
        return HttpResponseBadRequest("Faltan datos necesarios.")
    file = request.FILES.get('file', None)
    if file is None:
        return HttpResponseBadRequest("Faltan datos necesarios.")
    analysis = VTAnalysis(file=file)
    analysis.save()
    try:
        vt = VtHandler()
        results = vt.scan_file(analysis.file.path)
        if results is None:
            raise Exception()
        hash_obj = md5(analysis.file.path)
        analysis.harmless=results['resume_stats']['harmless']
        analysis.malicious=results['resume_stats']['malicious']
        analysis.suspicious=results['resume_stats']['suspicious']
        analysis.antiviruses_results=results['full_results']
        analysis.hash_obj=hash_obj
        analysis.save()
    except VtAPIKeyError:
        return JsonResponse({'analysis': None, 'error': "No se encontró una api key."})
    except Exception:
        analysis.file.delete()
        analysis.delete()
        vt.client.close()
        return JsonResponse({'analysis': None, 'error': "Ha ocurrido un error."})
    vt.client.close()
    return JsonResponse({'analysis': analysis.get_dict()})


def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()