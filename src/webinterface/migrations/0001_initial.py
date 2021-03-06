# Generated by Django 2.2.3 on 2019-07-18 05:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAuthenticate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrived_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('identification', models.CharField(help_text='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000', max_length=15, validators=[django.core.validators.RegexValidator('(^[1|5]\\d{11}$)|(^\\d{2}-\\d{4}-\\d{4}$)', message='Debe tener el formato 08-8888-8888 para nacionales o 500000000000 o 100000000000')])),
                ('request_datetime', models.DateTimeField(help_text="'%Y-%m-%d %H:%M:%S',   es decir  '2006-10-25 14:30:59'")),
                ('code', models.CharField(default='N/D', max_length=20)),
                ('status', models.IntegerField(default=0)),
                ('status_text', models.CharField(default='n/d', max_length=256)),
                ('sign_document', models.TextField(blank=True, null=True)),
                ('response_datetime', models.DateTimeField(auto_now=True)),
                ('expiration_datetime', models.DateTimeField()),
                ('id_transaction', models.IntegerField(db_index=True, default=0)),
                ('duration', models.SmallIntegerField(default=3)),
                ('received_notification', models.BooleanField(default=False)),
                ('resume', models.CharField(blank=True, max_length=250, null=True)),
                ('hash_docsigned', models.TextField(blank=True, null=True)),
                ('hash_id_docsigned', models.SmallIntegerField(default=0)),
            ],
        ),
    ]
