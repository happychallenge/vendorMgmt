# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-07 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cn_hscode',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='중국 HS CODE'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ko_hscode',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='한국 HS CODE'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='currency',
            field=models.CharField(choices=[('R', 'RMB'), ('$', 'DOLLAR')], default='$', max_length=1),
        ),
    ]