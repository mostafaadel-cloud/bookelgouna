# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0004_auto_20150331_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='adults',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='Adults', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apartment',
            name='children',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Children'),
            preserve_default=True,
        ),
    ]
