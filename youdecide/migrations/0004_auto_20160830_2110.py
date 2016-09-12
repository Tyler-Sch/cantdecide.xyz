# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0003_auto_20160830_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='active_time',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='total_time',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='yiel',
            field=models.IntegerField(default=None),
        ),
    ]
