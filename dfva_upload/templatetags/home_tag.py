from django import template
from dfva_upload.models import FileUpload

register = template.Library()


@register.simple_tag(takes_context=True)
def get_last_files(context):
    request = context['request']
    result = FileUpload.objects.filter(user=request.user).order_by('-created_on')
    if len(result) > 5:
        return result[:5]
    return result


