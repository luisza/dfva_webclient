from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from dfva_upload.models import FileUpload, VALIDATE_FORMAT
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import FileSign

# Create your views here.


@login_required
def manage_resume_view(request, fileid):
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid, user=request.user)
    if request.method == 'GET':
        filename = file_uploaded.filename.lower()

        last_resume = file_uploaded.filesign_set.latest('updated_on') if file_uploaded.filesign_set else None
        return render(request, 'fva_resume_form.html', {'fileid': fileid,
                                                        'is_pdf': filename.endswith('.pdf'),
                                                        'file_uploaded': file_uploaded,
                                                        'file_sign': last_resume})

    elif request.method == 'POST':
        file_extend = file_uploaded.filename.rsplit('.', 1)[1]
        resume = request.POST.get("resume")
        reason = request.POST.get("reason", None)
        place = request.POST.get("place", None)

        # Saves the sign form
        FileSign.objects.get_or_create(uploaded=file_uploaded,
                                       resume=resume,
                                       reason=reason,
                                       place=place,
                                       format=VALIDATE_FORMAT.get(file_extend, file_extend)
                                       )

        return redirect(reverse('file_sign', kwargs={'fileid': fileid}))
    else:
        raise Http404()


@login_required
def manage_download(request, fileid):
    file_sign = get_object_or_404(FileSign, uploaded__upload_id=fileid,  uploaded__user=request.user)
    if request.method == 'GET':
        # when the file hasn't a sign_document it should be signed before
        if not file_sign.sign_document:
            return redirect(reverse('file_resume', kwargs={'fileid': fileid}))

        return render(request, 'fva_download.html', {'fileid': fileid, 'file_signed': file_sign})
    raise Http404()


@login_required
def manage_sign(request, fileid):
    file_sign = get_object_or_404(FileSign, uploaded__upload_id=fileid, uploaded__user=request.user)
    if request.method == 'GET':
        return render(request, 'firmar.html', {'fileid': fileid,
                                               'filename': file_sign.uploaded.filename,
                                               'file_sign': file_sign})
    raise Http404()


@login_required
def sign_document_download(request, fileid):
    file_sign = get_object_or_404(FileSign, uploaded__upload_id=fileid, uploaded__user=request.user)
    if request.method == 'GET':
        if file_sign.sign_document:
            file_data = 'data:application/xml;base64,{}'.format(file_sign.sign_document)
            return HttpResponse(file_data)
    raise Http404()
