# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0034_auto_20150316_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='allotment',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Allotment', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='show_on_site',
            field=models.BooleanField(default=True, verbose_name='Show on site'),
            preserve_default=True,
        ),
    ]
