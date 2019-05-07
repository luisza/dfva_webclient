from django.db import models
from dfva_upload.models import FileUpload
# Create your models here.


class FileSign(models.Model):
    resume = models.CharField(max_length=255, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    sign_document = models.TextField(blank=True, null=True)
    uploaded = models.ForeignKey(FileUpload, null=False, blank=False, on_delete=models.CASCADE)

