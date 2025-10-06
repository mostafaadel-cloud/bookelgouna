# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantity', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
            preserve_default=True,
        ),
    ]
