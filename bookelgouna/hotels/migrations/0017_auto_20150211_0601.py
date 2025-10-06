# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0016_auto_20150211_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprice',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='Price', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
    ]
