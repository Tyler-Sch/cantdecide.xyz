# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0016_auto_20160929_1612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='amount',
            new_name='comment',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='display',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='other',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='qty',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(default='', max_length=100),
        ),
    ]
