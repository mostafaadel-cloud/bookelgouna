# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0011_roomprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='number_of_beds',
        ),
        migrations.AddField(
            model_name='room',
            name='adults',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='Adults', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='children',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Children'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='default_price',
            field=models.FloatField(default=0.0, verbose_name='Default price', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='area',
            field=models.FloatField(verbose_name='Area', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
    ]
