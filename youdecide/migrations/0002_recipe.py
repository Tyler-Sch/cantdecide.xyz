# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youdecide', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('url', models.TextField(default='')),
                ('title', models.TextField(default='')),
                ('ingredients', models.TextField(default='')),
                ('instructions', models.TextField(default='')),
                ('yiel', models.TextField(default='')),
                ('active_time', models.TextField(default='')),
                ('total_time', models.TextField(default='')),
            ],
        ),
    ]
