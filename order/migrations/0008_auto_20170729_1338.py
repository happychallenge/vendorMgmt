# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20170728_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paycondition',
            name='pay_term',
            field=models.CharField(choices=[('CASH', 'CASH'), ('30%PREPAY, 70%LATER', '30%PREPAY, 70%LATER'), ('T/T 30 DAYS', 'T/T 30 DAYS'), ('T/T 45 DAYS', 'T/T 45 DAYS'), ('T/T 60 DAYS', 'T/T 60 DAYS'), ('T/T 90 DAYS', 'T/T 90 DAYS')], max_length=20),
        ),
    ]
