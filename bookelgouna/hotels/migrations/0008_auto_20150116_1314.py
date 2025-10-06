# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_auto_20150116_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='has_air_conditioning',
            field=models.BooleanField(default=False, verbose_name='Has air conditioning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='has_sea_views',
            field=models.BooleanField(default=False, verbose_name='Has sea views'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='is_breakfast_included',
            field=models.BooleanField(default=False, verbose_name='Is breakfast included'),
            preserve_default=True,
        ),
    ]
