# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 00:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20170727_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='simple_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='SIMPLE NAME'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='en_name',
            field=models.CharField(max_length=50, verbose_name='ENGLISH NAME'),
        ),
    ]
