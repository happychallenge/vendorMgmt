# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-08 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_sourcing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourcing',
            old_name='rmbprice',
            new_name='buying_price',
        ),
        migrations.RenameField(
            model_name='sourcing',
            old_name='usdprice',
            new_name='sales_price',
        ),
    ]
