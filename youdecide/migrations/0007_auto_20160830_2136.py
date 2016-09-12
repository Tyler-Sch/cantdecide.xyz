# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0006_auto_20160830_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amounts',
            old_name='ingredientList',
            new_name='IList',
        ),
    ]
