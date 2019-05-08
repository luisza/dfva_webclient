from django.db import models
from chunked_upload.models import ChunkedUpload
# Create your models here.

VALIDATE_FORMAT = {'contrafirma': 'xml_contrafirma,',
                   'cofirma': 'xml_cofirma,',
                   'xml': 'cofirma',  # Todo: It should be confirmed
                   'odt': 'odf',
                   'ods': 'odf',
                   'odb': 'odf',
                   'docx': 'msoffice',
                   'xlsx': 'msoffice',
                   'pptx': 'msoffice',
                   'pdf': 'pdf'}


class FileUpload(ChunkedUpload):
    pass

# Override the default ChunkedUpload to make the `user` field nullable
FileUpload._meta.get_field('user').null=True
