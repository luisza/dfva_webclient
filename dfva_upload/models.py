from chunked_upload.models import ChunkedUpload
import mimetypes
# Create your models here.

VALIDATE_FORMAT = {'contrafirma': 'xml_contrafirma',
                   'cofirma': 'xml_cofirma',
                   'odt': 'odf',
                   'ods': 'odf',
                   'odb': 'odf',
                   'docx': 'msoffice',
                   'xlsx': 'msoffice',
                   'pptx': 'msoffice'}


class FileUpload(ChunkedUpload):
    def get_content_type(self):
        content_type, _ = mimetypes.guess_type(self.filename)
        return content_type
