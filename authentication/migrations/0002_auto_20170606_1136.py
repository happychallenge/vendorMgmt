# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 11:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='picture',
        ),
    ]
