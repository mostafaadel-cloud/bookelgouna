# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0005_auto_20150331_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='area',
            field=models.FloatField(default=42.0, verbose_name='Area', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
    ]
