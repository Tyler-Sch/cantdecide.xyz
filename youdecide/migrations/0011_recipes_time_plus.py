# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0010_auto_20160901_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='time_plus',
            field=models.CharField(max_length=1, default=''),
        ),
    ]
