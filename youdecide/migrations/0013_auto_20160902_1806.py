# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0012_auto_20160902_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('recipe', models.ForeignKey(to='youdecide.Recipes')),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='recipes',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='ingredient_l',
            field=models.ForeignKey(to='youdecide.Ingredient_list', default=''),
            preserve_default=False,
        ),
    ]
