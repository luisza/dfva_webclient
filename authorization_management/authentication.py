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
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(settings.DEFAULT_LOGGER_NAME)


@csrf_exempt
@require_http_methods(["POST"])
def login_with_bccr(request):
    identification = request.POST.get('Identificacion', '')
    if identification:
        authclient = ClienteAutenticador(settings.DEFAULT_BUSSINESS,
                                         settings.DEFAULT_ENTITY)

        print(authclient)
        if authclient.validar_servicio():
            data = authclient.solicitar_autenticacion(
                identification)

        else:
            logger.warning("Auth BCCR not available")
            data = authclient.DEFAULT_ERROR

        obj = AuthenticateDataRequest.objects.create(
            identification=identification,
            request_datetime=timezone.now(),
            expiration_datetime=timezone.now(
            ) - timezone.timedelta(int(data['tiempo_maximo'])),
        )

        request.session['authenticatedata'] = obj.pk

        success = data['codigo_error'] == settings.DEFAULT_SUCCESS_BCCR
        return JsonResponse({
            'FueExitosaLaSolicitud': success,
            'TiempoMaximoDeFirmaEnSegundos': 240,
            'TiempoDeEsperaParaConsultarLaFirmaEnSegundos': 2,
            'CodigoDeVerificacion': data['codigo_verificacion'],
            'IdDeLaSolicitud': data['id_solicitud'],
            'DebeMostrarElError': not success,
            'DescripcionDelError': data['texto_codigo_error'],
            'ResumenDelDocumento': data['resumen'] if "resumen" in data else ""

        })

    return Http404()


def consute_firma(request):
    callback = request.GET.get('callback')
    pk = request.GET.get('IdDeLaSolicitud', '')

    status = True
    status_text = ""
    realizada = 0
    if pk and callback:
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
                 "DescripcionDelError": status_text,
                 "FueExitosa": status,
                 "SeRealizo": realizada}
            )
        )
    )

