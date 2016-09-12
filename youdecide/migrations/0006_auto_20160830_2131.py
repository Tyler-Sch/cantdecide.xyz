# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0005_auto_20160830_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amounts',
            old_name='ingredient_list',
            new_name='ingredientList',
        ),
    ]
