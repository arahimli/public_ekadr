# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-09 11:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_auto_20170708_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyproductorservice',
            name='created_date',
            field=models.DateField(default=datetime.datetime(2017, 7, 9, 11, 47, 17, 205617, tzinfo=utc)),
        ),
    ]
