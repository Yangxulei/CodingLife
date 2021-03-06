# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-22 12:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_auto_20161112_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='avatar',
            field=models.URLField(default='static/images/default.png'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='createtime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
