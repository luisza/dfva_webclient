from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView

# Create your views here.

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import FileUpload

@login_required
def index(request):
    return render(request, 'index.html')

class UploadForm(TemplateView):
    template_name = 'dfva_upload_form.html'


class FileUploadView(ChunkedUploadView):
    model = FileUpload
    field_name = 'fva_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class FileUploadCompleteView(ChunkedUploadCompleteView):

    model = FileUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        pass

    def get_response_data(self, chunked_upload, request):
        return {'render': reverse('file_resume',
                                  kwargs={'fileid': chunked_upload.upload_id})}

