from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from webinterface.models import FileUpload


@login_required
def index(request):
    files = FileUpload.objects.filter(user = request.user).order_by('created_on')

    return render(request, 'index.html', {'files': files})