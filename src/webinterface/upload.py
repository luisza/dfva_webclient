import os
from base64 import b64encode

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from dfva_python.client import Client

from webinterface.forms import SignForm, ValidateForm, DownloadForm
from .models import FileUpload

class FileUploadView(ChunkedUploadView):
    model = FileUpload
    field_name = 'fva_file'

class FileUploadCompleteView(ChunkedUploadCompleteView):
    model = FileUpload

    def get_response_data(self, chunked_upload, request):
        return {'render': reverse('file_resume',
                                  kwargs={'fileid': chunked_upload.upload_id})}


@require_http_methods(["GET"])
def manage_uploaded_file(request, fileid):
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid, user = request.user)
    signform = SignForm(initial={'file_id': file_uploaded, 'identificacion': request.user.username,
                                 'doc_format': file_uploaded.get_extension()})
    validateform = ValidateForm(initial={'file_id': fileid,
                                         'doc_format': file_uploaded.get_extension()
                                         })
    return render(request, 'managefile.html', context={'fileid': fileid, 'tabactive': 'firmar',
                                                       'signform': signform,
                                                       'validateform': validateform,
                                                       'fileuploaded': file_uploaded})

@require_http_methods(["GET", 'POST'])
def delete_uploaded_file(request, fileid):
    if request.method == 'POST':
        f = FileUpload.objects.filter(upload_id=fileid).first()
        file_uploaded = get_object_or_404(FileUpload, upload_id=fileid,
                                          user=request.user)
        if file_uploaded.file:
            if os.path.isfile(file_uploaded.file.path):
                os.remove(file_uploaded.file.path)
        file_uploaded.delete()
        return HttpResponseRedirect('/')
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid, user = request.user)
    signform = SignForm(initial={'file_id': file_uploaded, 'identificacion': request.user.username,
                                 'doc_format': file_uploaded.get_extension()})
    validateform = ValidateForm(initial={'file_id': fileid,
                                         'doc_format': file_uploaded.get_extension()})
    return render(request, 'managefile.html', context={'fileid': fileid,
                                                       'tabactive': 'eliminar',
                                                       'signform': signform,
                                                       'validateform': validateform,
                                                       'fileuploaded': file_uploaded})
@require_http_methods(["POST"])
def validate_file(request):
    validateform = ValidateForm(request.POST)
    fileid = 0
    validacion = {}
    if validateform.is_valid():
        fileid = validateform.cleaned_data['file_id']
        file_uploaded = get_object_or_404(FileUpload, upload_id=fileid, user = request.user)

        signform = SignForm(initial={'file_id': file_uploaded, 'identificacion': request.user.username,
                                     'doc_format': file_uploaded.get_extension()})
        document = file_uploaded.file.read()
        document=  b64encode(document).decode()
        client = Client()
        validacion = client.validate(document, 'document', _format=validateform.cleaned_data['doc_format'])
    else:
        fileid = request.POST.get('file_id', '0')
        file_uploaded = get_object_or_404(FileUpload, upload_id=request.POST.get('file_id', '0'),
                                          user = request.user)
        signform = SignForm(initial={'file_id': file_uploaded,
                                     'identificacion': request.user.username,
                                     'doc_format': file_uploaded.get_extension()})
    return render(request, 'valida_managefile.html', context=
        {'fileid': fileid, 'tabactive': 'validar',
        'validacion': validacion,
        'signform': signform,
        'validateform': validateform,
        'fileuploaded': file_uploaded})


def download_uploaded_file(request, fileid):
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid, user = request.user)
    signform = SignForm(initial={'file_id': file_uploaded, 'identificacion': request.user.username,
                                 'doc_format': file_uploaded.get_extension()})
    validateform = ValidateForm(initial={'file_id': fileid, 'doc_format': file_uploaded.get_extension()})
    return render(request, 'download_managefile.html', context=
        {'fileid': fileid, 'tabactive': 'descargar',
        'signform': signform,
        'validateform': validateform,
        'fileuploaded': file_uploaded})



@require_http_methods(["POST"])
def direct_download_uploaded_file(request):
    form = DownloadForm(request.POST)
    if form.is_valid():
        file_uploaded = get_object_or_404(FileUpload, upload_id=form.cleaned_data['file_id'],
                                          user = request.user)
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"'%file_uploaded.filename
        file_uploaded.file.seek(0)
        response.write(file_uploaded.file.read())
        return response
    return Http404("File not found")