from django.http import Http404
from django.shortcuts import get_object_or_404, render
from dfva_upload.models import FileUpload, FORMATS
from dfva_python.client import Client
# Create your views here.


def manage_resume_view(request, fileid):
    file_uploaded = get_object_or_404(FileUpload, upload_id=fileid)

    if request.method == 'GET':
        render_view = "fva_resume_form.html"  # default form template
        # # pdf special form
        if file_uploaded.filename.endswith('pdf'):
            render_view = 'fva_pdf_resume_form.html'
        # normal form
        elif not file_uploaded.filename.endswith(tuple(FORMATS)):
            render_view = 'fva_warning_format.html'

        return render(request, render_view, {'fileid': fileid})

    elif request.method == 'POST':
        client = Client()

        return render(request, 'fva_pdf_resume_form.html', {'fileid': fileid})
    else:
        raise Http404()
