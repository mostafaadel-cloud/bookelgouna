# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0031_auto_20150313_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(unique=True, max_length=255, verbose_name='Slug'),
            preserve_default=True,
        ),
    ]
