# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0015_room_long_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='has_air_conditioning',
            field=models.BooleanField(default=False, verbose_name='Air conditioning'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='has_free_cancellation',
            field=models.BooleanField(default=False, verbose_name='Free cancellation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='has_sea_views',
            field=models.BooleanField(default=False, verbose_name='Sea views'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='is_breakfast_included',
            field=models.BooleanField(default=False, verbose_name='Breakfast included'),
            preserve_default=True,
        ),
    ]
