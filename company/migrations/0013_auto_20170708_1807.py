# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-08 14:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_auto_20170708_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyproductorservice',
            name='created_date',
            field=models.DateField(default=datetime.datetime(2017, 7, 8, 14, 7, 38, 339408, tzinfo=utc)),
        ),
    ]
