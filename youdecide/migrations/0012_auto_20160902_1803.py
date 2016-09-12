# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0011_recipes_time_plus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient_list',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='ingredientList',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipes',
            field=models.ForeignKey(default='', to='youdecide.Recipes'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Ingredient_list',
        ),
    ]
