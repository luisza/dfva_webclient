# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-08 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authenticatedatarequest',
            name='received_notification',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authenticatedatarequest',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='authenticatedatarequest',
            name='status_text',
            field=models.CharField(default='n/d', max_length=256),
        ),
    ]
