from django.conf.urls import url
from .views import manage_resume_view

urlpatterns = [
    url(r'^(?P<fileid>[0-9A-Za-z_\-]+)/resume/$', manage_resume_view, name='file_resume')
]


