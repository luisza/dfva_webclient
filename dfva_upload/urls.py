
from django.conf.urls import url
from django.urls import path

from .views import UploadForm, FileUploadView, FileUploadCompleteView

urlpatterns = [
    path('', UploadForm.as_view(), name='dfva_upload'),
    url(r'^upload/?$', FileUploadView.as_view(), name='dfva_uploading'),
    url(r'^upload_complete/?$', FileUploadCompleteView.as_view(),  name='dfva_upload_complete'),
]


