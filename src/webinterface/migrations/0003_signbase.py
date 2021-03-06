# Generated by Django 2.2.3 on 2019-07-20 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0002_fileupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion', models.CharField(max_length=20)),
                ('resumen', models.CharField(max_length=250)),
                ('doc_format', models.CharField(choices=[('xml_cofirma', 'XML sin firma'), ('xml_contrafirma', 'XML Firmado anteriormente'), ('odf', 'Open Document Format (Libreoffice)'), ('msoffice', 'Microsoft Office'), ('pdf', 'PDF')], default='pdf', max_length=10)),
                ('razon', models.CharField(blank=True, help_text='Requerido si firma PDF', max_length=250, null=True)),
                ('lugar', models.CharField(blank=True, help_text='Requerido si firma PDF', max_length=250, null=True)),
                ('id_transaction', models.IntegerField(default=0)),
                ('file_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webinterface.FileUpload')),
            ],
        ),
    ]
