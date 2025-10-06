# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0002_auto_20150330_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartmentpricecategory',
            options={'verbose_name': 'Apartment Price Category', 'verbose_name_plural': 'Apartment Price Categories'},
        ),
        migrations.AlterField(
            model_name='apartment',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Type', choices=[(1, 'Apartment'), (2, 'Villa')]),
            preserve_default=True,
        ),
    ]
