# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 10:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20170830_0642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourcing',
            old_name='saller_usd_price',
            new_name='seller_usd_price',
        ),
    ]
