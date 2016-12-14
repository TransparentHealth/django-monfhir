# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-13 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monfhir', '0002_auto_20161213_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportedresourcetype',
            name='self_only',
            field=models.BooleanField(default=False, help_text='This API is for a user only get their data'),
        ),
        migrations.AlterField(
            model_name='supportedresourcetype',
            name='collection_name',
            field=models.CharField(default='', help_text='MongoDB Collection Name', max_length=256),
        ),
    ]
