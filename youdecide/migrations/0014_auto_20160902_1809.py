# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0013_auto_20160902_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient_list',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='ingredient_l',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(to='youdecide.Recipes', default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Ingredient_list',
        ),
    ]
