# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0004_auto_20160830_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='active_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='total_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='yiel',
            field=models.IntegerField(default=0),
        ),
    ]
