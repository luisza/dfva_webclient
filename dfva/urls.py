"""dfva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls.base import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^files/', include('dfva_upload.urls')),
    url(r'^files/', include('dfva_sign_file.urls')),
    url(r'^accounts/login/$', LoginView.as_view(), {'redirect_to': reverse_lazy("dfva_upload")}, name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    #url(r'^', include('authorization_management.urls'), name='authorization_management')
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

