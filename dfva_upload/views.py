from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
# Create your views here.

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import FileUpload


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
        render_view = "file_sign"
        if request.session.get('authenticatedata', None):
            render_view = 'file_resume'
        return {'render': reverse(render_view,
                                  kwargs={'fileid': chunked_upload.upload_id})}

