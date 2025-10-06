# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0009_auto_20150409_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='min_nights_to_book',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Minimum number of nights to book', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
