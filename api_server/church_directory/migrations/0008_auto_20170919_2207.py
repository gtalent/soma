# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church_directory', '0007_auto_20170919_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='member',
            field=models.BooleanField(),
        ),
    ]
