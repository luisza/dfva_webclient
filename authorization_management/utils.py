from .models import AuthenticateDataRequest
from django.shortcuts import get_object_or_404


def get_identification(request, id):
    auth = get_object_or_404(AuthenticateDataRequest, id=id)
    return auth.identification
