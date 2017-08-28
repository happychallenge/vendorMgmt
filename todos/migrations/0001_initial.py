# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-25 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('duedate', models.DateField()),
                ('etype', models.CharField(choices=[('NORMAL', 'NORMAL'), ('URGENT', 'URGENT')], default='NORMAL', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
