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
from django.http.response import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from dfva_python.client import Client
from .models import AuthenticateDataRequest
from dfva_sign_file.models import FileSign

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


def call_login(identification):
    client = Client()
    auth_resp = client.authenticate(identification)
    data = client.authenticate_check(auth_resp['id_transaction'])

    auth = AuthenticateDataRequest.objects.create(
        identification=identification,
        status=data['status'],
        status_text=data['status_text'],
        received_notification=data['received_notification'],
        request_datetime=timezone.now(),
        expiration_datetime=data['expiration_datetime'],
    )
    return data, auth


def call_sign(identification, file_sign):
    client = Client()
    file_content = file_sign.uploaded.get_uploaded_file().read()

    sign_resp = client.sign(identification,
                            file_content,
                            file_sign.resume,
                            reason=file_sign.reason,
                            place=file_sign.place,
                            _format=file_sign.format)
    data = sign_resp
    if sign_resp.get('id_transaction', None):
        data = client.sign_check(sign_resp['id_transaction'])
        if data.get('id_transaction'):
            file_sign.sign_document = data.get('sign_document', None)
            file_sign.save()
    return data


@csrf_exempt
@require_http_methods(["POST"])
def login_with_bccr(request):
    identification = request.POST.get('Identificacion', '')
    if identification:
        data, auth = call_login(identification)
        request.session['authenticatedata'] = auth.pk
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
    authdata = AuthenticateDataRequest.objects.filter(identification=identification).first()

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


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def sign_with_bccr(request, fileid):
    file_sign = get_object_or_404(FileSign, uploaded__upload_id=fileid)

    sessionkey = None
    if 'authenticatedata' in request.session:
        sessionkey = request.session['authenticatedata']
    authdata = get_object_or_404(AuthenticateDataRequest, pk=sessionkey)

    data = call_sign(authdata.identification, file_sign)
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
