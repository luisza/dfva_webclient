from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from dfva_upload.models import FileUpload, VALIDATE_FORMAT
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import FileSign

# Create your views here.


@login_required
def manage_resume_view(request, fileid):
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid)
    if request.method == 'GET':
        filename = file_uploaded.filename.lower()
        is_pdf = False
        if filename.endswith('.pdf'):
            is_pdf = True
        return render(request, 'fva_resume_form.html', {'fileid': fileid, 'is_pdf': is_pdf})

    elif request.method == 'POST':
        file_extend = file_uploaded.filename.rsplit('.', 1)[1]
        resume = request.POST.get("resume")
        reason = request.POST.get("reason", None)
        place = request.POST.get("place", None)

        file_sign, created = FileSign.objects.get_or_create(uploaded=file_uploaded)
        file_sign.format = VALIDATE_FORMAT.get(file_extend, file_extend)
        file_sign.resume = resume
        file_sign.reason = reason
        file_sign.place = place
        file_sign.save()

        return redirect(reverse('file_sign', kwargs={'fileid': fileid}))
    else:
        raise Http404()


@login_required
def manage_download(request, fileid):
    file_sign = get_object_or_404(FileSign, uploaded__upload_id=fileid)
    if request.method == 'GET':
        return render(request, 'fva_download.html', {'fileid': fileid, 'file_signed': file_sign})
    raise Http404()


@login_required
def manage_sign(request, fileid):
    file_sign = get_object_or_404(FileSign, uploaded__upload_id=fileid)
    if request.method == 'GET':
        return render(request, 'firmar.html', {'fileid': fileid,
                                               'filename': file_sign.uploaded.filename,
                                               'file_sign': file_sign})
    raise Http404()


@login_required
def sign_document_download(request, fileid):
    file_sign = get_object_or_404(FileSign, uploaded__upload_id=fileid)
    if request.method == 'GET':
        if file_sign.sign_document:
            file_data = 'data:application/xml;base64,{}'.format(file_sign.sign_document)
            file_sign.delete()
            return HttpResponse(file_data)
    raise Http404()
