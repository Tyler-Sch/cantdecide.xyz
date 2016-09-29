# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0015_auto_20160929_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='active_time',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='total_time',
            field=models.CharField(default='', max_length=100),
        ),
    ]
