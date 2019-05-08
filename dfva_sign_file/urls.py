from django.conf.urls import url
from .views import manage_resume_view, manage_download, manage_sign

urlpatterns = [
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/resume/$', manage_resume_view, name='file_resume'),
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/download/$', manage_download, name='file_download'),
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/sign/$', manage_sign, name='file_sign')
]


