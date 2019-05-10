from django.db import models
from dfva_upload.models import FileUpload
# Create your models here.


class FileSign(models.Model):
    format = models.CharField(max_length=15, blank=True, null=True)
    resume = models.CharField(max_length=250, blank=True, null=True)
    reason = models.CharField(max_length=125, blank=True, null=True)
    place = models.CharField(max_length=150, blank=True, null=True)
    sign_document = models.TextField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    uploaded = models.ForeignKey(FileUpload, null=False, blank=False, on_delete=models.CASCADE)

