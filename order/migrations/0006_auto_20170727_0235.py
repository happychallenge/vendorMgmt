# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 02:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20170727_0013'),
        ('order', '0005_porder_contract_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='porderitem',
            unique_together=set([('porder', 'product', 'ptype')]),
        ),
    ]
