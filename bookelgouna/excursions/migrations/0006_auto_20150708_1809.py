# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0005_auto_20150708_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursionitemdiscountprice',
            name='discount_price',
            field=models.FloatField(verbose_name='Discount price per day', validators=[django.core.validators.MinValueValidator(0.01)]),
            preserve_default=True,
        ),
    ]
