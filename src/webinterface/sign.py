import json
from base64 import b64encode, b64decode

from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.core.files import File
import io

from webinterface.forms import SignForm, ValidateForm
from webinterface.models import SignBase, FileUpload
from dfva_python.client import Client


@csrf_exempt
@require_POST
def sign_terms_document(request, pk):
    obj = get_object_or_404(SignBase, pk=pk, file_id__user=request.user)
    client = Client()
    document =  obj.file_id.file.read()


    data = client.sign(obj.identificacion, document, obj.resumen, _format=obj.doc_format,
                place=obj.lugar, reason=obj.razon)

    success = data['status'] == settings.DEFAULT_SUCCESS_BCCR
    obj.id_transaction = data['id_transaction']
    obj.save()
    request.session['signed_doc'] = obj.pk
    return JsonResponse({
        'FueExitosaLaSolicitud': success,
        'TiempoMaximoDeFirmaEnSegundos': 240,
        'TiempoDeEsperaParaConsultarLaFirmaEnSegundos': 2,
        'CodigoDeVerificacion': data['code'],
        'IdDeLaSolicitud': data['id_transaction'],
        'DebeMostrarElError': not success,
        'DescripcionDelError': data['status_text'],
        'ResumenDelDocumento': obj.resumen

    })



def termsigned_check(request, pk):
    callback = request.GET.get('callback')
    id_transaction = request.GET.get('IdDeLaSolicitud', '')
    signdata = SignBase.objects.filter(
        pk=pk, file_id__user=request.user).first()

    sessionkey = None
    if 'signed_doc' in request.session:
        sessionkey = request.session['signed_doc']

    if signdata is None or signdata.pk != sessionkey:
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
    response_check = client.sign_check(id_transaction)
    status = response_check['status']

    status = response_check['status'] == settings.DEFAULT_SUCCESS_BCCR
    realizada = response_check['received_notification']
    if status and realizada:
        request.session.pop('signed_doc')
        uploadedfile = signdata.file_id
        uploadedfile.update_file(File(io.BytesIO(b64decode(response_check['sign_document']))))
        signdata.signed = True
        signdata.save()
    return HttpResponse(
        "%s(%s)" % (
            callback,
            json.dumps(
                {"ExtensionData": {},
                 "DebeMostrarElError": not status,
                 "DescripcionDelError": response_check['status_text'],
                 "FueExitosa": status,
                 "SeRealizo": realizada}
            )
        )
    )

@require_http_methods(["POST"])
def sign_file(request):
    fileid = 0

    signform = SignForm(request.POST)
    if signform.is_valid():
        signbase = signform.save()
        file_uploaded = signbase.file_id
        if file_uploaded.user != request.user:
            return HttpResponseForbidden()
        validateform = ValidateForm(initial={'file_id': file_uploaded.upload_id})
        return render(request, 'sign_managefile.html', context=
            {'fileid': file_uploaded.upload_id, 'tabactive': 'firmar',
         'signform': signform,
         'signbaseid': signbase.pk,
         'validateform': validateform,
         'fileuploaded': file_uploaded})

    file_uploaded = get_object_or_404(FileUpload,
                                      file_id__user=request.user,
                                      upload_id=request.POST.get('file_id', ''))
    validateform = ValidateForm(initial={'file_id': file_uploaded.upload_id})
    return render(request, 'managefile.html', context=
            {'fileid': file_uploaded.upload_id, 'tabactive': 'firmar',
             'signform': signform,
             'validateform': validateform,
             'fileuploaded': file_uploaded})