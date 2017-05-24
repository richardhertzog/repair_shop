# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dropoff', models.CharField(max_length=100)),
                ('pickup', models.CharField(max_length=100)),
                ('mechanic', models.CharField(max_length=50)),
                ('repair_type', models.CharField(max_length=10)),
            ],
        ),
    ]
