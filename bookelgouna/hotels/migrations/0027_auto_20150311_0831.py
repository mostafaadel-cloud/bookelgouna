# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0026_auto_20150311_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Slug'),
            preserve_default=True,
        ),
    ]
