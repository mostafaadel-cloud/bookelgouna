# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0049_room_cart_crop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roompricecategory',
            name='regular_price',
            field=models.FloatField(default=66, verbose_name='Regular Price', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=False,
        ),
    ]
