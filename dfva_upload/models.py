from django.db import models
from chunked_upload.models import ChunkedUpload
# Create your models here.

FORMATS = ['xml', 'odt', 'ods', 'odb', 'docx', 'xlsx', 'pptx', 'pdf']


class FileUpload(ChunkedUpload):
    pass


# Override the default ChunkedUpload to make the `user` field nullable
FileUpload._meta.get_field('user').null=True
