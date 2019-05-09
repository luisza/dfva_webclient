from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import AuthenticateDataRequest


def home(request):
    return render(request, 'index.html')


def logout_view(request):
    if 'authenticatedata' in request.session:
        sessionkey = request.session['authenticatedata']
        authdata = AuthenticateDataRequest.objects.filter(pk=sessionkey)
        authdata.delete()

    logout(request)
    return redirect('home')

