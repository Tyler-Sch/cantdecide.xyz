# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0002_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amounts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('how_much', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('item', models.CharField(default='', max_length=100)),
                ('amounts', models.ManyToManyField(to='youdecide.Amounts')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient_list',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Instructions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('step', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('url', models.URLField(default='')),
                ('title', models.CharField(default='', max_length=200)),
                ('yiel', models.IntegerField()),
                ('active_time', models.IntegerField()),
                ('total_time', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='instructions',
            name='recipe',
            field=models.ForeignKey(to='youdecide.Recipes'),
        ),
        migrations.AddField(
            model_name='ingredient_list',
            name='recipe',
            field=models.ForeignKey(to='youdecide.Recipes'),
        ),
        migrations.AddField(
            model_name='amounts',
            name='ingredient_list',
            field=models.ManyToManyField(to='youdecide.Ingredient_list'),
        ),
    ]
