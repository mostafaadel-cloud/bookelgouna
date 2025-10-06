# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0006_apartment_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentpricecategory',
            name='regular_price',
            field=models.FloatField(default=66, verbose_name='Regular Price', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=False,
        ),
    ]
