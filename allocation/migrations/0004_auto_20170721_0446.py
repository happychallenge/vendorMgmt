# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 04:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_sourcing_sales_price'),
        ('allocation', '0003_auto_20170719_1209'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='demand',
            unique_together=set([('product', 'year', 'month')]),
        ),
        migrations.AlterUniqueTogether(
            name='demandclient',
            unique_together=set([('demand', 'client')]),
        ),
    ]
