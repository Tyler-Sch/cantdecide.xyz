# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0017_auto_20161026_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='comment',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='item',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='other',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='qty',
            field=models.CharField(max_length=100, default=''),
        ),
    ]
