from django.db import models
from chunked_upload.models import ChunkedUpload
# Create your models here.

VALIDATE_FORMAT = {'contrafirma': 'contrafirma,',
                   'cofirma': 'xml_cofirma,',
                   'odt': 'odf',
                   'ods': 'odf',
                   'odb': 'odf',
                   'docx': 'msoffice',
                   'xlsx': 'msoffice',
                   'pptx': 'msoffice'}


class FileUpload(ChunkedUpload):
    pass
