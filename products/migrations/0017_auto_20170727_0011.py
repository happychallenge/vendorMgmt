# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 00:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20170726_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='en_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='SIMPLE NAME'),
        ),
    ]