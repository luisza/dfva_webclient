from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import AuthenticateDataRequest


def home(request):
    return render(request, 'index.html')


def logout_view(request):
    if 'authenticatedata' in request.session:
        request.session.pop('authenticatedata')

    logout(request)
    return redirect('home')

