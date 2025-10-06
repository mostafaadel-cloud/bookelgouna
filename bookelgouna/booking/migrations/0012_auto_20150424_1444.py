# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_auto_20150421_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='item_based_product',
            field=models.BooleanField(default=False, verbose_name='Item Based Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item_based_product',
            field=models.BooleanField(default=False, verbose_name='Item Based Product'),
            preserve_default=True,
        ),
    ]
