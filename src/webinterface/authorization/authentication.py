# encoding: utf-8

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
@date: 16/6/2018
@author: Luis Zarate Montero
@contact: luis.zarate@solvosoft.com
@license: GPLv3
'''

from django.http.response import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging
from django.views.decorators.http import require_http_methods
import json
from django.utils import timezone
from django.contrib.auth import authenticate, login
from dfva_python.client import Client

from webinterface.models import BaseAuthenticate

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


@csrf_exempt
@require_http_methods(["POST"])
def login_with_bccr(request):
    identification = request.POST.get('Identificacion', '')
    if identification:
        client = Client()
        data = client.authenticate(identification)

        obj = BaseAuthenticate.objects.create(
            identification=identification,
            request_datetime= data['request_datetime'],
            code=data['code'],
            status=data['status'],
            status_text=data['status_text'],
            response_datetime =  timezone.now(),
            expiration_datetime = data['expiration_datetime'],
            id_transaction = data['id_transaction'],
            duration = data['duration'],
            resume =data['resumen'] if "resumen" in data else ""
        )


        request.session['authenticatedata'] = obj.pk

        success = data['status'] == settings.DEFAULT_SUCCESS_BCCR
        return JsonResponse({
            'FueExitosaLaSolicitud': success,
            'TiempoMaximoDeFirmaEnSegundos': 360,
            'TiempoDeEsperaParaConsultarLaFirmaEnSegundos': 2,
            'CodigoDeVerificacion': data['code'],
            'IdDeLaSolicitud': data['id_transaction'],
            'DebeMostrarElError': not success,
            'DescripcionDelError': data['status_text'],
            'ResumenDelDocumento': data['resumen'] if "resumen" in data else ""

        })

    return Http404()


def consute_firma(request):
    callback = request.GET.get('callback')
    pk = request.GET.get('IdDeLaSolicitud', '')
    authdata = BaseAuthenticate.objects.filter(
        id_transaction=pk).first()

    sessionkey = None
    if 'authenticatedata' in request.session:
        sessionkey = request.session['authenticatedata']

    if authdata is None or authdata.pk != sessionkey:
        return HttpResponse(
            "%s(%s)" % (
                callback,
                json.dumps(
                    {"ExtensionData": {},
                     "DebeMostrarElError": True,
                     "DescripcionDelError": "Transacción inexistente",
                     "FueExitosa": False,
                     "SeRealizo": True}
                )
            )
        )
    client = Client()
    auth_response = client.authenticate_check(code=pk)
    status = auth_response['status'] == settings.DEFAULT_SUCCESS_BCCR
    realizada = auth_response['received_notification']
    if realizada:
        authdata.received_notification = auth_response['received_notification']
        authdata.status = auth_response['status']
        authdata.status_text = auth_response['status_text']
        authdata.hash_docsigned = auth_response['hash_docsigned']
        authdata.hash_id_docsigned = auth_response['hash_id_docsigned']
        authdata.sign_document = auth_response['sign_document']
        authdata.save()
    if status and realizada:
        request.session.pop('authenticatedata')
        user = authenticate(token=pk)
        if user is not None:
            login(request, user)
    return HttpResponse(
        "%s(%s)" % (
            callback,
            json.dumps(
                {"ExtensionData": {},
                 "DebeMostrarElError": not status,
                 "DescripcionDelError": auth_response['status_text'],
                 "FueExitosa": status,
                 "SeRealizo": realizada}
            )
        )
    )


def login_index(request):
    return render(request, 'login_index.html')