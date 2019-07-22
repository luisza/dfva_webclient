from django import forms

from webinterface.models import SignBase, FileUpload


class SignForm(forms.ModelForm):
    class Meta:
        model = SignBase
        fields = '__all__'
        exclude = ['id_transaction', 'signed']
        widgets = {
            'file_id': forms.HiddenInput()
        }


class ValidateForm(forms.Form):
    EXTENSIONS = (
        ('cofirma', 'XML sin firma'),
        ('contrafirma', 'XML Firmado anteriormente'),
        ('odf', 'Open Document Format (Libreoffice)'),
        ('msoffice', 'Microsoft Office'),
        ('pdf', 'PDF')
    )
    doc_format = forms.ChoiceField(choices=EXTENSIONS)
    file_id = forms.CharField(max_length=250, widget=forms.HiddenInput)

class DownloadForm(forms.Form):
    file_id = forms.CharField(max_length=250, widget=forms.HiddenInput)