from django.urls import path
from .views import *


urlpatterns = [
    path('get-by-hash/<str:hash_obj>', get_analysis_by_hash),
    path('upload/', upload_file),
]