# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-07 20:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dfva_upload', '0003_auto_20190507_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileupload',
            name='place',
        ),
        migrations.RemoveField(
            model_name='fileupload',
            name='reason',
        ),
        migrations.RemoveField(
            model_name='fileupload',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='fileupload',
            name='sign_document',
        ),
    ]
