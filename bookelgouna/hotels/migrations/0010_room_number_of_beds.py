# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0009_room_has_free_cancellation'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='number_of_beds',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Number of beds', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
