from django.conf.urls import url
from .views import manage_resume, manage_download, manage_sign, sign_document_download

urlpatterns = [
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/resume/$', manage_resume, name='file_resume'),
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/download/$', manage_download, name='file_download'),
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/signdownload/$', sign_document_download, name='sign_document_download'),
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/sign/$', manage_sign, name='file_sign')
]


