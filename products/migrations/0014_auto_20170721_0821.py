# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_sourcing_sales_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='contact_profile/'),
        ),
    ]
