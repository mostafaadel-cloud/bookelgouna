# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0003_auto_20150409_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportitemtranslation',
            name='title',
            field=models.CharField(default='stub', max_length=255, verbose_name='Title'),
            preserve_default=False,
        ),
    ]
