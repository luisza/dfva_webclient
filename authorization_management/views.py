from authorization_management.models import AuthorizationRequest
from django.shortcuts import render


# Create your views here.
def authorize_user_request(request):
    objs=AuthorizationRequest.objects.filter(
        finished=False
    )
    return render(
        request,
        'authorization_request.html',
        {'object_list': objs}
    )
