# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0050_auto_20150403_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotel',
            options={'verbose_name': 'Hotel', 'verbose_name_plural': 'HOTELS'},
        ),
        migrations.AlterField(
            model_name='hotelcomment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='is approved'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roompricecategorytranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category Name:'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='hotelreview',
            unique_together=set([('service', 'reviewer')]),
        ),
    ]
