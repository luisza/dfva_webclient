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

import json
import logging
from django.views.decorators.http import require_http_methods
from pyfva.clientes.autenticador import ClienteAutenticador
from django.http.response import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import AuthenticateDataRequest
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from dfva_python.client import Client
import random

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


@csrf_exempt
@require_http_methods(["POST"])
def login_with_bccr(request):
    identification = request.POST.get('Identificacion', '')
    if identification:
        client = Client()
        auth_resp = client.authenticate(identification)
        data = client.authenticate_check(auth_resp['id_transaction'])

        obj = AuthenticateDataRequest.objects.create(
            identification=identification,
            status=data['status'],
            status_text=data['status_text'],
            received_notification=data['received_notification'],
            request_datetime=timezone.now(),
            expiration_datetime=data['expiration_datetime'],
        )

        request.session['authenticatedata'] = obj.pk

        success = data['status'] == settings.DEFAULT_SUCCESS_BCCR
        return JsonResponse({
            'FueExitosaLaSolicitud': success,
            'TiempoMaximoDeFirmaEnSegundos': 240,
            'TiempoDeEsperaParaConsultarLaFirmaEnSegundos': 2,
            'CodigoDeVerificacion': data['code'],
            'IdDeLaSolicitud': data['identification'],
            'DebeMostrarElError': not success,
            'DescripcionDelError': data['status_text'],
            'ResumenDelDocumento': data['resumen'] if "resumen" in data else ""

        })
    return Http404()


@csrf_exempt
def consute_firma(request):
    callback = request.GET.get('callback')
    identification = request.GET.get('IdDeLaSolicitud', '')
    authdata = AuthenticateDataRequest.objects.filter(
        identification=identification).order_by('-request_datetime').first()

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

    status = authdata.status == settings.DEFAULT_SUCCESS_BCCR
    realizada = authdata.received_notification
    if status and realizada:
        # request.session.pop('authenticatedata')
        user = authenticate(token=identification)
        if user is not None:
            login(request, user)
    return HttpResponse(
        "%s(%s)" % (
            callback,
            json.dumps(
                {"ExtensionData": {},
                 "DebeMostrarElError": not status,
                 "DescripcionDelError": authdata.status_text,
                 "FueExitosa": status,
                 "SeRealizo": realizada}
            )
        )
)
