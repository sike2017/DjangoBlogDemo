# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-12 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20180107_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='markdown_content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
