# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0008_auto_20160831_0057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('item', models.CharField(default='', max_length=100)),
                ('amount', models.CharField(default='', max_length=100)),
                ('original_txt', models.TextField(default='')),
                ('ingredientList', models.ForeignKey(to='youdecide.Ingredient_list')),
            ],
        ),
    ]
