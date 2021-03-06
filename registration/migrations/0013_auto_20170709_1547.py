# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-09 11:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20170708_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='changeprofileinfo',
            name='admin_reject',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 7, 9, 11, 47, 17, 260982, tzinfo=utc), editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='reset_key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 7, 9, 11, 47, 17, 260982, tzinfo=utc), editable=False, null=True),
        ),
    ]
