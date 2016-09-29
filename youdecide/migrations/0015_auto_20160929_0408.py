# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0014_auto_20160902_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='imgUrl',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='active_time',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='total_time',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='yiel',
            field=models.CharField(default='', max_length=100),
        ),
    ]
