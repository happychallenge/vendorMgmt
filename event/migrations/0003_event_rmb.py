# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20170729_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rmb',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]