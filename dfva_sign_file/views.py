from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from dfva_upload.models import FileUpload, VALIDATE_FORMAT
from dfva_python.client import Client
from .models import FileSign
from authorization_management.utils import get_identification
# Create your views here.


def get_resume_template(file_uploaded):
    render_view = "fva_resume_form.html"  # default form template
    filename = file_uploaded.filename.lower()

    # # pdf special form
    if filename.endswith('pdf'):
        render_view = 'fva_pdf_resume_form.html'
    # normal form
    elif not filename.endswith(tuple(VALIDATE_FORMAT.keys())):
        file_uploaded.delete()
        render_view = 'fva_warning_format.html'
    return render_view


def manage_resume_view(request, fileid):
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid)
    if request.method == 'GET':
        render_view = get_resume_template(file_uploaded)
        return render(request, render_view, {'fileid': fileid})

    elif request.method == 'POST':
        client = Client()
        file_content = file_uploaded.get_uploaded_file().read()
        file_extend = file_uploaded.filename.rsplit('.', 1)[1]
        authid = request.session['authenticatedata']

        resume = request.POST.get("resume")
        reason = request.POST.get("reason", None)
        place = request.POST.get("place", None)

        sign_resp = client.sign(get_identification(request, authid),
                                file_content,
                                resume,
                                _format=VALIDATE_FORMAT.get(file_extend),
                                reason=reason,
                                place=place)

        render_download = False
        if sign_resp.get('id_transaction'):
            data = client.sign_check(sign_resp['id_transaction'])
            if data.get('id_transaction'):
                file_sign = FileSign()
                file_sign.sign_document = data.get('sign_document', None)
                file_sign.resume = resume
                file_sign.reason = reason
                file_sign.place = place
                file_sign.uploaded = file_uploaded

                file_sign.save()
                render_download = True
                # client.sign_delete(data['id_transaction'])

        if render_download:
            return render(request, 'fva_download.html', {'fileid': fileid, 'filename': file_uploaded.filename})
        else:
            render_view = get_resume_template(file_uploaded)
            return render(request, render_view, {'fileid': fileid, 'error': sign_resp.get('status_text', None)})
    else:
        raise Http404()


def manage_download(request, fileid):
    file_uploaded = get_object_or_404(FileSign, uploaded__upload_id=fileid)
    print(file_uploaded.uploaded.__dict__)
    if file_uploaded.sign_document:
        file_data = 'data:application/xml;base64,{}'.format(file_uploaded.sign_document)
        # file_uploaded.delete()
        return HttpResponse(file_data)
    else:
        raise Http404()


def manage_sign(request, fileid):
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid)
    if request.method == 'GET':
        return render(request, 'firmar.html', {'fileid': fileid, 'filename': file_uploaded.filename})
    raise Http404()
