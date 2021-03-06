# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-20 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('phone_number_code', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='general.Region')),
            ],
        ),
    ]
