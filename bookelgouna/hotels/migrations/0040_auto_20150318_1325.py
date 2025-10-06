# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0039_roompricecategory_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='default_price',
        ),
        migrations.AlterField(
            model_name='room',
            name='allotment',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Allotment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roompricecategory',
            name='regular_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Regular Price', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
    ]
