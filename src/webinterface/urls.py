from django.urls import path, re_path
from webinterface import views
from webinterface.authorization  import authentication
from webinterface.sign import sign_terms_document, termsigned_check, sign_file
from webinterface.upload import FileUploadView, FileUploadCompleteView, manage_uploaded_file, validate_file, \
    download_uploaded_file, direct_download_uploaded_file, delete_uploaded_file

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/login/', authentication.login_index, name='login'),
    path('login_fd', authentication.login_with_bccr, name='login_fd'),
    path("consute_firma", authentication.consute_firma, name='consute_firma'),

    path('valida_documento', validate_file, name='validate_file'),
    re_path(r'^(?P<fileid>[0-9A-Za-z_\-]+)/delete/$', delete_uploaded_file, name='delete_uploaded_file'),
    re_path(r'^(?P<fileid>[0-9A-Za-z_\-]+)/resume/$', manage_uploaded_file, name='file_resume'),
    re_path(r'^upload/?$', FileUploadView.as_view(), name='dfva_uploading'),
    re_path(r'^upload_complete/?$', FileUploadCompleteView.as_view(), name='dfva_upload_complete'),

    re_path(r'^download/file$', direct_download_uploaded_file, name="direct_download_file"),
    re_path(r'^download/(?P<fileid>[0-9A-Za-z_\-]+)', download_uploaded_file, name="download_file"),

    re_path(r'^sign_file$', sign_file, name="sign_file"),
    re_path(r'^firme/(?P<pk>\d+)$', sign_terms_document, name="sign_terms_document"),
    re_path(r'^firme/check/(?P<pk>\d+)$', termsigned_check, name="termsigned_check"),

]
