# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-11 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20170711_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='packing',
            name='ptype',
            field=models.CharField(choices=[('POWDER', 'POWDER'), ('GRANULAR', 'GRANULAR'), ('LIQUID', 'LIQUID')], default='POWDER', max_length=10),
        ),
    ]
