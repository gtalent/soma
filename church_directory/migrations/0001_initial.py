# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('person', models.IntegerField(primary_key=True, serialize=False)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('picture', models.ImageField(upload_to='person/pictures')),
            ],
        ),
    ]
