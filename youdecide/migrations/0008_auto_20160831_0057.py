# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0007_auto_20160830_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amounts',
            name='IList',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='amounts',
        ),
        migrations.DeleteModel(
            name='Amounts',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
