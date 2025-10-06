# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0004_excursionitemdiscountprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursionitemdiscountprice',
            name='number_of_days',
            field=models.SmallIntegerField(verbose_name='Number of days', validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(30)]),
            preserve_default=True,
        ),
    ]
