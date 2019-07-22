from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _
from chunked_upload.models import ChunkedUpload


identification_validator = RegexValidator(
    r'(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)',
    message=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000"))

# Create your models here.
class BaseAuthenticate(models.Model):
    arrived_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    identification = models.CharField(
        max_length=15, validators=[identification_validator],
        help_text=_("Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000")
    )
    # '%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'
    request_datetime = models.DateTimeField(
        help_text=_("""'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'"""))
    code = models.CharField(max_length=20, default='N/D')
    status = models.IntegerField(default=0)
    status_text = models.CharField(max_length=256, default='n/d')
    sign_document = models.TextField(null=True, blank=True)
    response_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField()
    id_transaction = models.IntegerField(default=0, db_index=True)
    duration = models.SmallIntegerField(default=3)
    received_notification = models.BooleanField(default=False)
    resume = models.CharField(max_length=250, null=True, blank=True)
    hash_docsigned = models.TextField(null=True, blank=True)
    hash_id_docsigned = models.SmallIntegerField(default=0)



VALIDATE_FORMATs = ['xml', 'odt', 'ods', 'odb', 'docx', 'xlsx', 'pptx', 'pdf']





class FileUpload(ChunkedUpload):
    def update_file(self, binarydata):
        #self.file.close()
        #self.file.open('wb')
        self.offset = 0
        self.file.seek(0)
        #self.file.close()
        self._md5 = None
        self.append_chunk(binarydata, len(binarydata), save=True)


    def get_extension(self):
        options = {
            'pdf': 'pdf',
            'doc': 'msoffice',
            'xls': 'msoffice',
            'docx': 'msoffice',
            'xlsx': 'msoffice',
            'ppt': 'msoffice',
            'odt': 'odf',
            'fodt': 'odf',
            'ods': 'odf',
            'fods': 'odf',
            'odp': 'odf',
            'fodp': 'odf',
            'odg': 'odf',
            'fodg': 'odf',
            'xml': 'xml_cofirma'
        }

        dev = 'pdf'

        filename = self.filename.split('.')

        if len(filename) > 1:
            ext = filename[-1]
            ext = ext.lower()

            if ext in options:
                dev = options[ext]


        return dev

class SignBase(models.Model):
    EXTENSIONS = (
        ('xml_cofirma', 'XML sin firma'),
        ('xml_contrafirma', 'XML Firmado anteriormente'),
        ('odf', 'Open Document Format (Libreoffice)'),
        ('msoffice', 'Microsoft Office'),
        ('pdf', 'PDF')
    )
    file_id = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=20)
    resumen = models.CharField(max_length=250)
    doc_format = models.CharField(max_length=10, choices=EXTENSIONS, default='pdf')
    razon = models.CharField(max_length=250, null=True, blank=True, help_text='Requerido si firma PDF')
    lugar = models.CharField(max_length=250, null=True, blank=True, help_text='Requerido si firma PDF')
    id_transaction = models.IntegerField(default=0)
    signed = models.BooleanField(default=False)